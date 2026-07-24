"""
Admin configuration for notifications app.
"""

from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""

    list_display = [
        "notification_type",
        "recipient_email",
        "status",
        "subject",
        "sent_at",
        "created_at",
    ]
    list_filter = ["notification_type", "status", "sent_at", "created_at"]
    search_fields = ["subject", "recipient_email"]
    ordering = ["-created_at"]
    readonly_fields = ["sent_at", "created_at", "updated_at"]
