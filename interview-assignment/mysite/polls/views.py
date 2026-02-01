from django.shortcuts import render
from rest_framework.views import APIView
from  rest_framework.response import Response
from .models import Customer, Order, VisitCount, Restaurant
from .serializers import CustomerSerializer, CustomerRegisterSerializer, OrderSerializer,VisitSerializer, RestaurantReadSerializer, RestaurantWriteSerializer
import logging 
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