from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "product_name",
            "amount",
            "currency",
            "shipping_city",
            "shipping_country",
            "status",
            "risk_score",
            "risk_reason",
            "external_trace_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "risk_score",
            "risk_reason",
            "external_trace_id",
            "created_at",
            "updated_at",
        ]