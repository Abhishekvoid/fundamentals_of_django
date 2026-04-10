from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.serializers import OrderSerializer
from .services.service import OrderService
from core.tasks import process_order_risk


class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        task = process_order_risk.delay(order.id)

        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "status": order.status,
                "task_id": task.id,
            },
            status=status.HTTP_201_CREATED,
        )