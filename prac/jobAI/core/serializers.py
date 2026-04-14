from rest_framework import serializers
from .models import JobPosting, ApplicationDraft


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "company",
            "location",
            "job_type",
            "source_url",
            "description",
            "required_skills",
            "match_score",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "match_score",
            "status",
            "created_at",
            "updated_at",
        ]


class ApplicationDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDraft
        fields = [
            "id",
            "job",
            "cover_letter",
            "outreach_message",
            "draft_status",
            "generated_at",
        ]
        read_only_fields = [
            "id",
            "cover_letter",
            "outreach_message",
            "draft_status",
            "generated_at",
        ]