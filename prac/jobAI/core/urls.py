from django.urls import path
from .views import JobPostingListCreateView, ApplicationDraftListView

urlpatterns = [
    path("jobs/", JobPostingListCreateView.as_view(), name="job-list-create"),
    path("drafts/", ApplicationDraftListView.as_view(), name="draft-list"),
]