from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class JobPosting(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        ANALYZED = "analyzed", "Analyzed"
        APPLIED = "applied", "Applied"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_postings")
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=120)
    job_type = models.CharField(max_length=50, blank=True, default="")
    source_url = models.URLField()
    description = models.TextField()
    required_skills = models.JSONField(default=list, blank=True)
    match_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class ApplicationDraft(models.Model):
    class DraftStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        GENERATED = "generated", "Generated"
        SENT = "sent", "Sent"

    job = models.OneToOneField(JobPosting, on_delete=models.CASCADE, related_name="application_draft")
    cover_letter = models.TextField(blank=True, default="")
    outreach_message = models.TextField(blank=True, default="")
    draft_status = models.CharField(max_length=20, choices=DraftStatus.choices, default=DraftStatus.PENDING)
    generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Draft for {self.job.title}"
