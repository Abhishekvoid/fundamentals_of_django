from rest_framework import serializers
from .models import AppUser, MenuItem, order

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields  = ['phone_number', 'username']

    def validate_phonenumber(self, value):

        if not value.startswith("+91"):
            raise serializers.ValidationError("phone number should have correct code")
        return value
    
class MenuSerailizer