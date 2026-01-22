from django.urls import path, include
from .views import QuestionListCreateAPIView, QuestionDetailAPIView, ChoiceCreateAPiView

urlpatterns = [
     
    path("questions/", QuestionListCreateAPIView.as_view(), name="questions"),
    path("questions/<int:pk>/", QuestionDetailAPIView.as_view()),
    path("choices/", ChoiceCreateAPiView.as_view(), name="choices")
]
