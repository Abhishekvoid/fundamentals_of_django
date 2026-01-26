from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class AppUser(models.Model):

    phone_number = PhoneNumberField(primary_key = True)
    username  = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.username

class MenuItem(models.Model):

    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(blank=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    items = models.JSONField()
    total_price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.items
    
class VisitCount(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.visits