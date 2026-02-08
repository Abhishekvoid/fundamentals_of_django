from django.shortcuts import render
from rest_framework.views import APIView
from  rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer
from rest_framework import status
import logging 
logger = logging.getLogger(__name__)


class RegisterUserView(APIView):


    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
