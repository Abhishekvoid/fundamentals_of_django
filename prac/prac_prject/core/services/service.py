from dataclasses import dataclass
from decimal import Decimal

from core.models import Order


@dataclass
class RiskPayload:
    order_id: int
    user_id: int
    amount: float
    currency: str
    shipping_city: str
    shipping_country: str
    product_name: str


class OrderService:
    @staticmethod
    def create_order(*, user, validated_data) -> Order:
        order = Order.objects.create(
            user=user,
            product_name=validated_data["product_name"],
            amount=validated_data["amount"],
            currency=validated_data.get("currency", "INR"),
            shipping_city=validated_data["shipping_city"],
            shipping_country=validated_data.get("shipping_country", "India"),
            status=Order.Status.PENDING,
        )
        return order

    @staticmethod
    def build_risk_payload(order: Order) -> RiskPayload:
        return RiskPayload(
            order_id=order.id,
            user_id=order.user_id,
            amount=float(order.amount),
            currency=order.currency,
            shipping_city=order.shipping_city,
            shipping_country=order.shipping_country,
            product_name=order.product_name,
        )

    @staticmethod
    def mark_processing(order: Order) -> None:
        order.status = Order.Status.PROCESSING
        order.save(update_fields=["status", "updated_at"])

    @staticmethod
    def apply_risk_result(*, order: Order, risk_score: float, risk_reason: str) -> Order:
        order.risk_score = risk_score
        order.risk_reason = risk_reason
        order.status = Order.Status.FLAGGED if risk_score >= 0.75 else Order.Status.APPROVED
        order.save(update_fields=["risk_score", "risk_reason", "status", "updated_at"])
        return order