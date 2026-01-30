from asgiref.sync import sync_to_async
from django.db.models import Avg
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import AppUser, MenuItem, Order, VisitCount
from .serializers import UserRegisterSerializer, MenuSerailizer, OrderSerializer
import time
import asyncio
import logging 
logger = logging.getLogger(__name__)


class UserRegisterView(APIView):

    def post(self, request):

        serializer  = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class MenuView(APIView):

    def get(self, request):
        items = MenuItem.objects.filter(available = True)
        serializer = MenuSerailizer(items, many=True)
        return Response (serializer.data )
    
    def post(self, request):

        serializer  = MenuSerailizer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
    

class UserOrderAPIView(APIView):
    def get(self, request, phone):
        try:
            user = AppUser.objects.get(phone_number  = phone)
            order = Order.objects.filter(user=user)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        except AppUser.DoesNotExist:
            return Response({"error": "user not found"}, 404)

class UserStatsView(APIView):
    def get(self, request, phone):
        try:
            user = AppUser.objects.get(phone_number = phone)
            visit_Count = VisitCount.objects.get(user=user).visits
            orders = Order.objects.filter(user=user)
            avg_order = orders.aggregate(avg=Avg('total_price'))['avg'] or 0
            return Response({

                "visits": visit_Count,
                "total_orders": orders.count(),
                "avg_order_value": round(avg_order, 2)
            })
        except AppUser.DoesNotExist:
            return Response({'error': 'user not found'}, 404)

class RestaurantListView(APIView):

    async def get(self, request):

        await asyncio.sleep(2)
        data = [
            {"name": "Pizza Palace", "rating": 4.5, "time": "30 mins"},
            {"name": "Curry House", "rating": 4.8, "time": "45 mins"},
            {"name": "Burger King", "rating": 4.2, "time": "25 mins"}
        ]

        return Response(data)

class UserProfileView(APIView):
    
    async def get(self, request):

        await asyncio.sleep(0.5)
        data = {
            "username": "Abhishek",
            "email": "abhishek@example.com",
            "orders_count": 52
        }

        return Response(data)

class GoldStatusView(APIView):

    async def get(self, request):

        await asyncio.sleep(3)
        data = {
            "is_gold": True,
            "expiry": "2025-12-31",
            "benefits": ["Free Delivery", "Priority Support"]
        }

        return Response(data)

class UserVisitStatus(APIView):

    async def get(self, request, phone):

        try:
            user = await sync_to_async(AppUser.objects.get)(
                phone_number = phone
            )
            
            visit = await sync_to_async(VisitCount.objects.get)(
                user=user
            )

            avg_order = await sync_to_async(Order.objects.filter(user=user).aggregate)(avg=Avg("total_price"))
       

            return Response ( {

                "username": user.username,
                "visit_count": visit.visits,
                "avg_order_value": avg_order['avg'] or 0
            }, status=status.HTTP_202_ACCEPTED)

        except AppUser.DoesNotExist:
            return Response({"error": "user not found"}, status=404)