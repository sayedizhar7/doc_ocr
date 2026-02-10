from django.contrib import admin
from .models import ValidationRequest

@admin.register(ValidationRequest)
class ValidationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "doc_type", "doc_number", "holder_name", "status", "created_at")
    list_filter = ("doc_type", "status", "created_at")
    search_fields = ("doc_number", "holder_name", "user__username", "user__email")

