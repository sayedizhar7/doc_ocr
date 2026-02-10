from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.action(description="Approve selected users")
def approve_users(modeladmin, request, queryset):
    for u in queryset:
        u.set_status(User.Status.APPROVED)

@admin.action(description="Decline selected users")
def decline_users(modeladmin, request, queryset):
    for u in queryset:
        u.set_status(User.Status.DECLINED)

@admin.action(description="Suspend selected users")
def suspend_users(modeladmin, request, queryset):
    for u in queryset:
        u.set_status(User.Status.SUSPENDED)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Business Info", {"fields": ("full_name", "contact", "company_name", "company_address")}),
        ("Approval", {"fields": ("status", "status_updated_at")}),
    )
    list_display = ("username", "email", "full_name", "status", "is_active", "date_joined")
    list_filter = ("status", "is_active")
    actions = [approve_users, decline_users, suspend_users]

