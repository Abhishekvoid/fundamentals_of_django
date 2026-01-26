from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import AppUser, MenuItem, Order, VisitCount
from .serializers import UserRegisterSerializer, MenuSerailizer, OrderSerializer
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