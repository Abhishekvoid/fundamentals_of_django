# core/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        APPROVED = "approved", "Approved"
        FLAGGED = "flagged", "Flagged"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    shipping_city = models.CharField(max_length=120)
    shipping_country = models.CharField(max_length=120, default="India")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    risk_score = models.FloatField(null=True, blank=True)
    risk_reason = models.TextField(blank=True, default="")
    external_trace_id = models.CharField(max_length=120, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product_name}"