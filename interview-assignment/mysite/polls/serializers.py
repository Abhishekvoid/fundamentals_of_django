from rest_framework import serializers
from .models import Customer, Order, Restaurant, VisitCount
import secrets

# -------------------------
# Customer
# -------------------------


class CustomerRegisterSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField()
    name = serializers.CharField(required = False)

    def validate_phone_numer(self, value):

        if not str(value).startwith("+91"):
            raise serializers.ValidationError("phone number must start with +91")
        return value
    
    def create(self, validate_data):
        phone = validate_data["phone_number"]
        name = validate_data.get("name", "")

        customer, created = Customer.objects.get_or_create(

            phone_number= phone,
            defaults={"name": name}
        )

        if not customer.auth_token:
            customer.auth_token = secrets.token_hex(32)
            customer.save()

        return customer
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['phone_number', 'name']

    def validate_phone_number(self, value):
        if not str(value).startswith("+91"):
            raise serializers.ValidationError("Phone number must start with +91")
        return value


# -------------------------
# Restaurant

# -------------------------
class RestaurantReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'city', 'is_active']
        read_only_fields = fields


class RestaurantWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['name', 'city']


# -------------------------
# Visit
# -------------------------
class VisitSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = VisitCount
        fields = ['customer', 'restaurant', 'visited_at']
        read_only_fields = ['visited_at']


# -------------------------
# Order
# -------------------------
class OrderSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Order
        fields = ['customer', 'restaurant', 'items', 'total_amount']
        read_only_fields = ['total_amount']

    def validate_items(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list")

        for item in value:
            if 'price' not in item or 'qty' not in item:
                raise serializers.ValidationError(
                    "Each item must contain price and qty"
                )
        return value

    def create(self, validated_data):
        items = validated_data.pop('items')

        total = sum(
            item['price'] * item['qty']
            for item in items
        )

        order = Order.objects.create(
            total_amount=total,
            **validated_data
        )

        return order
