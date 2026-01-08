from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name = "index")
]


"""
    next step: to configure the root URLconfig in basics porject to include the this URLconf from the app: go to project/urls.py 
"""