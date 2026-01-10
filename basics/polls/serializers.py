from rest_framework import serializers
from .models import Question, AppUser, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "votes"]

class QuestionSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "choices"]

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model: AppUser
        fields = ["username", "email", "is_active"]

"""
- serializer = schema + validation + tranformation
- this Replaces:
    - manual dict building
    - manual validation
- interviews LOVE serializers
"""