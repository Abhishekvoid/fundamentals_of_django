
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/polls/", include("polls.urls"))       # importing the app urls to the root project urls
   
]
