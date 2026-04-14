from rest_framework import generics, permissions
from .models import JobPosting, ApplicationDraft
from .serializers import JobPostingSerializer, ApplicationDraftSerializer


class JobPostingListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPosting.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationDraftListView(generics.ListAPIView):
    serializer_class = ApplicationDraftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApplicationDraft.objects.filter(
            job__user=self.request.user
        ).select_related("job").order_by("-generated_at")