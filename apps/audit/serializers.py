"""
Serializers for audit app.
"""

from rest_framework import serializers

from apps.audit.models import AuditLog, AuditLogArchive


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "user_role",
            "action",
            "action_display",
            "entity_type",
            "entity_id",
            "old_data",
            "new_data",
            "changed_fields",
            "ip_address",
            "user_agent",
            "request_method",
            "request_path",
            "description",
            "reason",
            "timestamp",
            "created_at",
        ]
        read_only_fields = ["id", "timestamp", "created_at"]


class AuditLogArchiveSerializer(serializers.ModelSerializer):
    """Serializer for AuditLogArchive model."""

    action_display = serializers.CharField(source="get_action_display", read_only=True)

    class Meta:
        model = AuditLogArchive
        fields = [
            "id",
            "user_email",
            "user_role",
            "action",
            "action_display",
            "entity_type",
            "entity_id",
            "old_data",
            "new_data",
            "changed_fields",
            "ip_address",
            "user_agent",
            "description",
            "reason",
            "original_timestamp",
            "archived_at",
            "created_at",
        ]
        read_only_fields = ["id", "archived_at", "created_at"]
