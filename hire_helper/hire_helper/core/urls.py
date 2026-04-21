# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, BookingReadOnlyViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="booking-create")
router.register("booking-feed", BookingReadOnlyViewSet, basename="booking-feed")

urlpatterns = [
    path("api/", include(router.urls)),
]