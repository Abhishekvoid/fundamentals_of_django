from django.db import models
import uuid


class CustomUser(models.Model):
    
    user_id = models.UUIDField(default=uuid.uuid4, blank=False)
    name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=50)


    def __str__(self):
        return self.name
