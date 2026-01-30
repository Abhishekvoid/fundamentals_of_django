from rest_framework import serializers
from .models import Customer, Order, Restaurant, VisitCount

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customer
        fields = ['phone_number', 'name']
        read_only_fields = ['phone_number']

        def validate_Phone_Number(self, value):

            if not value.startswith("+91"):
                raise serializers.ValidationError("phone number should have correct code")
            return value
    
class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:

        model = Restaurant
        fields = ['name', 'city', 'is_active']
        read_only_fields = ['name', 'city']
        

