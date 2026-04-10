import random
from celery import shared_task
from django.db import transaction

from core.models import Order
from .services.service import OrderService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def process_order_risk(self, order_id: int):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(id=order_id)
        OrderService.mark_processing(order)

    payload = OrderService.build_risk_payload(order)

    risk_score = _mock_ai_risk_engine(payload)
    risk_reason = _build_reason(payload, risk_score)

    with transaction.atomic():
        fresh_order = Order.objects.select_for_update().get(id=order_id)
        OrderService.apply_risk_result(
            order=fresh_order,
            risk_score=risk_score,
            risk_reason=risk_reason,
        )

    return {
        "order_id": order_id,
        "risk_score": risk_score,
        "status": "flagged" if risk_score >= 0.75 else "approved",
    }


def _mock_ai_risk_engine(payload) -> float:
    score = 0.10

    if payload.amount > 50000:
        score += 0.35
    if payload.shipping_country.lower() != "india":
        score += 0.25
    if "gift card" in payload.product_name.lower():
        score += 0.20
    if payload.shipping_city.lower() in {"unknown", "test"}:
        score += 0.15

    score += random.uniform(0.01, 0.08)
    return min(round(score, 2), 0.99)


def _build_reason(payload, risk_score: float) -> str:
    if risk_score >= 0.75:
        return "High-value or suspicious shipping pattern detected by risk rules."
    return "Order looks normal under baseline risk checks."