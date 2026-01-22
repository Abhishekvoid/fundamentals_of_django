from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Question, Choices, AppUser, InvalidVoteError
from .serializers import QuestionSerializer, ChoiceSerializer, AppUserSerializer
import logging 
logger = logging.getLogger(__name__)


class QuestionListCreateAPIView(APIView):

    def get(self, request):
        questions  = Question.objects.all()
        serializer  = QuestionSerializer(questions, many= True)
        return Response(serializer.data)
    

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChoiceCreateAPiView(APIView):

    def get(self, request):
        choices = Choices.objects.all()
        
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
          return Choices.objects.all()
    
    def post(self, request):
        try:

            serializer = ChoiceSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 201)
        except InvalidVoteError as e:
            logger.error(f"Vote error: {e}")
            return Response({"error": str(e)}, 400)
        except Exception as e:
            logger.error(f"Unexpected: {e}")
            return Response({"error": "Server error"}, 500)
    
class QuestionDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
