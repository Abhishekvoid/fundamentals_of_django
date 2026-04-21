from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingCreateSerializer, BookingResponseSerializer
from .orchestrator import BookingOrchestrator, BookingOrchestrationError


class BookingViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = BookingOrchestrator().create_booking(**serializer.validated_data)
        except BookingOrchestrationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(BookingResponseSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.select_related("assigned_worker").all().order_by("-created_at")
    serializer_class = BookingResponseSerializer