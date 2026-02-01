from django.urls import path
from .views import (
    CustomerRegisterView, CustomerListView, CreateOrderView, 
    CreateRestaurantView, RestaurantListView, CreateVisitView, 
    AsyncCustomerDashboardView, AsyncCustomerStats
)

urlpatterns = [
    # Customer Management
    path('register/', CustomerRegisterView.as_view(), name="register"),
    path('customerlist/', CustomerListView.as_view(), name='customer-list'),
    
    # Order Management  
    path('createorder/', CreateOrderView.as_view(), name='order-create'),
    
    # Restaurant Management
    path('createrestaurant/', CreateRestaurantView.as_view(), name='restaurant-create'),
    path('restaurantlist/', RestaurantListView.as_view(), name='restaurant-list'),
    
    # Visit Tracking
    path('createvisit/', CreateVisitView.as_view(), name="visit-create"),
    
    # ASYNC AGGREGATION 
    path('dashboard/<str:phone>/', AsyncCustomerDashboardView.as_view(), name='customer-dashboard'),
    path('stats/<str:phone>/', AsyncCustomerStats.as_view(), name='customer-stats'),
]
