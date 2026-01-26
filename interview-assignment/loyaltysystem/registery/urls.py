from django.urls import path, include
from .views import UserRegisterSerializer, MenuView, OrderCreateAPIView, UserOrderAPIView, UserStatsView


urlpatterns = [
    
    path('register/', UserRegisterSerializer, name='register'),

    path('menu/', MenuView.as_view(), name='menu'),

    path('order/', OrderCreateAPIView.as_view(), name='order-create'),

    path('user/<str:phone>/orders/', UserOrderAPIView.as_view(), name='user-orders'),

    path('user/<str:phone>/stats/', UserStatsView.as_view(), name='user-stats')
]   
