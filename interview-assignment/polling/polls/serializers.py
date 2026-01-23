from rest_framework import serializers
from .models import Question, Choices, AppUser


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model: AppUser
        fields = ["username", "email", "is_active"]
    
    def validate_email(self, value):

        if not value.endswith("@example.com"):
            raise serializers.ValidationError("Email must belong to @example.com")
        return value
    
class ChoiceSerializer(serializers.ModelSerializer):

    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all()
    )
    
    class Meta:
        model = Choices
        fields = ["choice_id", "question", "choice_text", "votes"]  

    def validate_votes(self, value):
        if value < 0:
            raise serializers.ValidationError("Votes cannot be nagivate")
        
    def validate_question(self, data):
        question = data["question"]
        if question.is_expired:
            raise serializers.ValidationError("Question expired 7 days after publish_date")
        return data
    
class QuestionSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ["question_id", "question_text", "publish_date", "choices"]

class VoteTooHighError(Exception):
    pass

def vote(choice_id, votes):
    if votes > 1000:
        raise VoteTooHighError(f"Max 1000 votes, got{votes}")