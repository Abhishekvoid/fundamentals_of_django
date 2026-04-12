from django.urls import path, include
from .views import CreateOrderView, DriverLocationUpdateView


urlpatterns = [
    path("orders/", CreateOrderView.as_view(), name="orders"),
    path("DriverLocation/", DriverLocationUpdateView.as_view(), name="Driver Location" )
]
