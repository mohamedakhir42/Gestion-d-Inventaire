"""
Admin configuration for audit app.
"""

from django.contrib import admin

from apps.audit.models import AuditLog, AuditLogArchive


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for AuditLog model."""

    list_display = [
        "action",
        "entity_type",
        "user_email",
        "user_role",
        "timestamp",
        "ip_address",
    ]
    list_filter = ["action", "entity_type", "user_role", "timestamp"]
    search_fields = ["user_email", "entity_type", "description", "reason"]
    ordering = ["-timestamp"]
    readonly_fields = [
        "user",
        "user_email",
        "user_role",
        "action",
        "entity_type",
        "entity_id",
        "old_data",
        "new_data",
        "changed_fields",
        "ip_address",
        "user_agent",
        "request_method",
        "request_path",
        "timestamp",
    ]


@admin.register(AuditLogArchive)
class AuditLogArchiveAdmin(admin.ModelAdmin):
    """Admin interface for AuditLogArchive model."""

    list_display = [
        "action",
        "entity_type",
        "user_email",
        "original_timestamp",
        "archived_at",
    ]
    list_filter = ["action", "entity_type", "original_timestamp", "archived_at"]
    search_fields = ["user_email", "entity_type", "description"]
    ordering = ["-original_timestamp"]
    readonly_fields = [
        "user_email",
        "user_role",
        "action",
        "entity_type",
        "entity_id",
        "old_data",
        "new_data",
        "changed_fields",
        "ip_address",
        "user_agent",
        "original_timestamp",
        "archived_at",
    ]
