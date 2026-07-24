"""
Admin configuration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import LoginHistory, Permission, RolePermission, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ["email", "get_full_name", "employee_id", "role", "status", "is_active", "last_login", "created_at"]
    list_filter = ["role", "status", "is_active", "department", "created_at"]
    search_fields = ["email", "first_name", "last_name", "employee_id"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "invitation_token", "invitation_sent_at", "invitation_accepted_at", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone", "avatar")}),
        ("Employee Info", {"fields": ("employee_id", "department", "position")}),
        ("Role & Status", {"fields": ("role", "status", "is_staff", "is_active")}),
        ("Invitation", {"fields": ("invitation_token", "invitation_sent_at", "invitation_accepted_at", "terms_accepted", "terms_accepted_at")}),
        ("Tracking", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "employee_id",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin interface for Permission model."""

    list_display = ["name", "codename", "module", "created_at"]
    list_filter = ["module", "created_at"]
    search_fields = ["name", "codename", "description"]
    ordering = ["module", "name"]


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """Admin interface for RolePermission model."""

    list_display = ["role", "permission", "granted_at"]
    list_filter = ["role", "granted_at"]
    ordering = ["-granted_at"]


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin interface for LoginHistory model."""

    list_display = ["user", "ip_address", "login_time", "logout_time", "status"]
    list_filter = ["status", "login_time"]
    search_fields = ["user__email", "ip_address"]
    ordering = ["-login_time"]
    readonly_fields = ["login_time"]
