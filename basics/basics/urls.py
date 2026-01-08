"""
URL configuration for basics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("polls/", include("polls.urls"))       # importing the app urls to the root project urls

    
]


"""
path():
    - function expects at least two arguments: route and view.

include(): 
    - function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

    # When to use include()

        - You should always use include() when you include other URL patterns. The only exception is   admin.site.urls, which is a pre-built URLconf provided by Django for the default admin site.


        Now you can run this project using: python manage.py runserver
"""