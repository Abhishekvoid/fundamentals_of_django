from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Question, Choice, AppUser
from .serializers import QuestionSerializer, ChoiceSerializer, AppUserSerializer


class QuestionListCreateAPIView(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceCreateAPiView(APIView):

    def get_choices(self, request):
        choices = Choice.objects.all()
        
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
          return Choice.objects.all()
    
    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

- most basic view you can build, to acces it in browser -> we need to map it to URL
- There URl configurations are define in each django app, and they are file named urls.py

"""