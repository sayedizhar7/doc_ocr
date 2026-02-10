from django.db import models
from django.conf import settings

class DocumentType(models.TextChoices):
    PAN = "PAN", "PAN"
    AADHAAR = "AADHAAR", "Aadhaar"
    GST = "GST", "GST"
    FSSAI = "FSSAI", "FSSAI"
    MSME = "MSME", "MSME"

class ValidationRequest(models.Model):
    class Status(models.TextChoices):
        VALID = "VALID", "Valid"
        INVALID = "INVALID", "Invalid"
        ERROR = "ERROR", "Error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="validation_requests")
    doc_type = models.CharField(max_length=20, choices=DocumentType.choices)
    doc_number = models.CharField(max_length=80, blank=True)
    holder_name = models.CharField(max_length=200, blank=True)
    uploaded_file = models.FileField(upload_to="uploads/%Y/%m/%d/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ERROR)
    api_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
