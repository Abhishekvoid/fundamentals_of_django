from rest_framework import serializers
from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=100)
    service_type = serializers.ChoiceField(
        choices=[
            "cleaning",
            "laundry",
            "utensil_washing",
            "cooking_help",
            "babysitting",
            "elder_care",
            "bathroom_cleaning",
        ]
    )
    address = serializers.CharField()
    scheduled_at = serializers.DateTimeField()
    duration_hours = serializers.IntegerField(min_value=1, max_value=12)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if "test" in attrs["address"].lower():
            raise serializers.ValidationError("Please provide a valid service address")
        return attrs


class BookingResponseSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source="assigned_worker.full_name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer_id",
            "service_type",
            "scheduled_at",
            "duration_hours",
            "status",
            "estimated_price",
            "final_price",
            "worker_name",
            "created_at",
        ]