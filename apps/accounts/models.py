from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"
        SUSPENDED = "SUSPENDED", "Suspended"

    full_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=30)
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    status_updated_at = models.DateTimeField(default=timezone.now)

    def set_status(self, new_status: str):
        self.status = new_status
        self.status_updated_at = timezone.now()
        self.is_active = (new_status == self.Status.APPROVED)
        self.save(update_fields=["status", "status_updated_at", "is_active"])

