from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta



class InvalidVoteError(Exception):
    pass

class  QuestionExpiredError(Exception):
    pass

class Question(models.Model):
    question_text = models.CharField(max_length=256)
    publish_date = models.DateTimeField("data published")
    author = models.CharField(max_length = 256)

    @property
    def is_expired(self):
        return timezone.now() > (self.publish_date + timedelta(days=7))

    def __str__(self):
        return self.question_text
    
class Choices(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="chocies")
    choices_text =  models.CharField(max_length=256)
    vote = models.IntegerField(default=0)

    def add_vote(self):
        if self.vote > 1000:
            raise InvalidVoteError("Max 1000 votes allowed")
        self.vote += 1
        self.save()
        
    def __str__(self):
        return self.choices_text
    
class AppUser(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    username =  models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=264)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

