from dataclasses import dataclass
from decimal import Decimal
from django.db.models import Q
from .models import WorkerProfile, WorkerAvailability


@dataclass
class MatchCandidate:
    worker: WorkerProfile
    score: float


class WorkerMatchingService:
    def find_candidates(self, *, service_type, scheduled_at, duration_hours, city):
        qs = (
            WorkerProfile.objects.filter(
                status=WorkerProfile.Status.ACTIVE,
                is_verified=True,
                city__iexact=city,
            )
        )

        results = []
        for worker in qs:
            if service_type not in worker.service_types:
                continue

            slot_exists = WorkerAvailability.objects.filter(
                worker=worker,
                start_at__lte=scheduled_at,
                end_at__gte=scheduled_at,
                is_booked=False,
            ).exists()

            if slot_exists:
                score = round(worker.trust_score * 0.7 + 0.3, 2)
                results.append(MatchCandidate(worker=worker, score=score))

        return sorted(results, key=lambda item: item.score, reverse=True)


class PricingService:
    BASE_RATES = {
        "cleaning": Decimal("249.00"),
        "laundry": Decimal("199.00"),
        "utensil_washing": Decimal("149.00"),
        "cooking_help": Decimal("299.00"),
        "babysitting": Decimal("399.00"),
        "elder_care": Decimal("499.00"),
        "bathroom_cleaning": Decimal("349.00"),
    }

    def estimate(self, *, service_type, duration_hours):
        base = self.BASE_RATES[service_type]
        return base * Decimal(duration_hours)


class WorkerAssignmentService:
    def reserve_slot(self, worker, scheduled_at):
        slot = WorkerAvailability.objects.filter(
            worker=worker,
            start_at__lte=scheduled_at,
            end_at__gte=scheduled_at,
            is_booked=False,
        ).first()

        if not slot:
            raise ValueError("No slot available")

        slot.is_booked = True
        slot.save(update_fields=["is_booked"])
        return slot


class PaymentService:
    def authorize(self, booking):
        return {"payment_state": "authorized", "booking_id": str(booking.id)}

    def capture_and_split(self, booking):
        platform_fee = booking.final_price * Decimal("0.15")
        worker_payout = booking.final_price - platform_fee
        return {
            "platform_fee": str(platform_fee),
            "worker_payout": str(worker_payout),
            "status": "settled",
        }