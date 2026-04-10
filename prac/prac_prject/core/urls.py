from django.urls import path, include
from .views import CreateOrderView


urlpatterns = [
    path("orders/", CreateOrderView.as_view(), name="orders"),
]
