import uuid
from decimal import Decimal
from django.db import models


class WorkerProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        ACTIVE = "active"
        SUSPENDED = "suspended"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=80)
    service_types = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    trust_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkerAvailability(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name="slots")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_booked = models.BooleanField(default=False)


class Booking(models.Model):
    class Status(models.TextChoices):
        SEARCHING = "searching"
        AWAITING_WORKER = "awaiting_worker"
        CONFIRMED = "confirmed"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        CANCELLED = "cancelled"
        EXPIRED = "expired"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50)
    address = models.TextField()
    scheduled_at = models.DateTimeField()
    duration_hours = models.PositiveIntegerField()
    notes = models.TextField(blank=True, default="")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SEARCHING)
    assigned_worker = models.ForeignKey(
        WorkerProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings"
    )
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)


class BookingEvent(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="events")
    step = models.CharField(max_length=100)
    status = models.CharField(max_length=30)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

