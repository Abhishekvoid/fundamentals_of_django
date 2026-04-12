from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        
class DriverLocationUpdateView(APIView):
    
    def post(self, request, order_id):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            f"order_{order_id}",
            {
                "type": "location_update",
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        
        return Response(
            {"message": "Location update sent successfully"},
            status=status.HTTP_200_OK
        )