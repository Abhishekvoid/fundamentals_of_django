from rest_framework import serializers
from .models import AppUser, MenuItem, Order, VisitCount

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields  = ['phone_number', 'username']

    def validate_phone_number(self, value):

        if not value.startswith("+91"):
            raise serializers.ValidationError("phone number should have correct code")
        return value
    
class MenuSerailizer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = ["name", "price", "available"]

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.all())

    class Meta:
        model = Order
        fields = ["user", "items", "total_price"]
    
    def create(self, validated_data):
        
        items = validated_data['items']
        total = sum(item['price'] * item['qty'] for item in items)
        validated_data['total_price'] = total

        order = order.objects.create(**validated_data)

        visit, created = VisitCount.objects.get_or_create(

            user=validated_data['user'], 
            defaults={'visits': 0}
        )
        visit.visits += 1
        visit.save()

        return order