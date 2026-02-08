from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation  import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required=True, validator=[validate_password])

    model = CustomUser
    fields = ['name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    
    def validate_email(self, value):

        if "@" not in value or "." not in value:
            raise serializers.ValidationError("enter valid email address")
        return value
    
    def validate_existing(self, attrs):

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('user alredy exists')
        return attrs