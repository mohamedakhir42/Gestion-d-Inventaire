"""
Serializers for notifications app.
"""

from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""

    recipient_name = serializers.CharField(source="recipient.get_full_name", read_only=True)
    type_display = serializers.CharField(source="get_notification_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "recipient_name",
            "recipient_email",
            "notification_type",
            "type_display",
            "status",
            "status_display",
            "subject",
            "body",
            "data",
            "sent_at",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "sent_at", "created_at", "updated_at"]
