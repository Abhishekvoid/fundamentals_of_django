from django.shortcuts import render
from rest_framework.views import APIView
from  rest_framework.response import Response
from .models import Customer, Order, VisitCount, Restaurant
from .serializers import CustomerSerializer, CustomerRegisterSerializer, OrderSerializer,VisitSerializer, RestaurantReadSerializer, RestaurantWriteSerializer
import logging 
import asyncio
from asgiref.sync import sync_to_async
from django.db.models import Avg, Count
logger = logging.getLogger(__name__)



class CustomerRegisterView(APIView):

    def post(self, request):

        serializer = CustomerRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        return Response({
            "phone_number": customer.phone_number,
            "token": customer.auth_token
        })

class CustomerListView(APIView):

    def get(self, request):

        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many = True)
        return Response(serializer.data)


class RestaurantListView(APIView):

    def get(self, request):

        restaurant = Restaurant.objects.all()
        serializer = RestaurantReadSerializer(restaurant, many=True)
        return Response(serializer.data)
    
class CreateRestaurantView(APIView):
    def post(self,request):

        serializer = RestaurantWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant = serializer.save()

        return Response(serializer.data, status=201)
class CreateVisitView(APIView):

    def post(self, request):

        serializer = VisitSerializer(data = request.data)
        
        serializer.is_valid(raise_exception=True)
        
        visit = serializer.save()
        return Response(serializer.data, status=201)
       

class CreateOrderView(APIView):

    def post(self, request):

        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(serializer.data, status=201)
    

class AsyncCustomerDashboardView(APIView):

    async def get(self, request, phone):

        customers, orders, restaurants, visits = await asyncio.gather(

            sync_to_async(lambda: Customer.objects.filter(phone_number=phone))(),
            sync_to_async(lambda:Restaurant.objects.filter(is_active=True))(),
            sync_to_async(lambda:Order.objects.filter(customer=phone))(),
            sync_to_async(lambda:VisitCount.objects.filter(customer=phone))()
            
        )

        return Response({

            'profile': CustomerSerializer(customers, many=True).data,
            'restaurants': RestaurantReadSerializer(restaurants, many=True).data,
            'orders': OrderSerializer(orders, many=True).data,
            'visits': VisitSerializer(visits, many=True).data   
        })
    

class AsyncCustomerStats(APIView):

    async def get(self, request, phone):

        customer = await sync_to_async(Customer.objects.get)(
            phone_number = phone
        )
        
        visits_task = await sync_to_async(VisitCount.objects.filter(customer=customer).count)()

        avg_order_task = await sync_to_async(Order.objects.filter(customer=customer).aggregate)(avg=Avg("total_amount"))

        visits, avg_order = await visits_task, await avg_order_task

        return Response({
            "customer": customer.name,
            "visits": visits,
            "avg_order_value": avg_order["avg"] or 0
        })