from django.db import transaction
from .models import Booking, BookingEvent
from .services import (
    WorkerMatchingService,
    PricingService,
    WorkerAssignmentService,
    PaymentService,
)


class BookingOrchestrationError(Exception):
    pass


class BookingOrchestrator:
    def __init__(self):
        self.matching = WorkerMatchingService()
        self.pricing = PricingService()
        self.assignment = WorkerAssignmentService()
        self.payment = PaymentService()

    def _event(self, booking, step, status, payload=None):
        BookingEvent.objects.create(
            booking=booking,
            step=step,
            status=status,
            payload=payload or {},
        )

    @transaction.atomic
    def create_booking(self, *, customer_id, service_type, address, scheduled_at, duration_hours, notes=""):
        city = "Ahmedabad"  # in production derive from address / geo service

        booking = Booking.objects.create(
            customer_id=customer_id,
            service_type=service_type,
            address=address,
            scheduled_at=scheduled_at,
            duration_hours=duration_hours,
            notes=notes,
            status=Booking.Status.SEARCHING,
        )
        self._event(booking, "booking_created", "completed")

        candidates = self.matching.find_candidates(
            service_type=service_type,
            scheduled_at=scheduled_at,
            duration_hours=duration_hours,
            city=city,
        )
        if not candidates:
            booking.status = Booking.Status.EXPIRED
            booking.save(update_fields=["status"])
            self._event(booking, "worker_matching", "failed", {"reason": "no_worker_found"})
            raise BookingOrchestrationError("No workers available for this slot")

        selected = candidates[0].worker
        self._event(
            booking,
            "worker_matching",
            "completed",
            {"worker_id": str(selected.id), "score": candidates[0].score},
        )

        self.assignment.reserve_slot(selected, scheduled_at)
        booking.assigned_worker = selected
        booking.status = Booking.Status.AWAITING_WORKER
        booking.estimated_price = self.pricing.estimate(
            service_type=service_type,
            duration_hours=duration_hours,
        )
        booking.save(update_fields=["assigned_worker", "status", "estimated_price"])
        self._event(
            booking,
            "slot_reserved",
            "completed",
            {"worker_id": str(selected.id), "estimated_price": str(booking.estimated_price)},
        )

        payment_result = self.payment.authorize(booking)
        self._event(booking, "payment_authorized", "completed", payment_result)

        booking.status = Booking.Status.CONFIRMED
        booking.final_price = booking.estimated_price
        booking.save(update_fields=["status", "final_price"])
        self._event(booking, "booking_confirmed", "completed")

        return booking

    @transaction.atomic
    def mark_completed(self, booking: Booking):
        booking.status = Booking.Status.COMPLETED
        booking.save(update_fields=["status"])
        settlement = self.payment.capture_and_split(booking)
        self._event(booking, "payment_settlement", "completed", settlement)
        self._event(booking, "job_completed", "completed")
        return booking