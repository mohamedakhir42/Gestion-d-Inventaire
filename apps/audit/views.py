"""
API views for audit app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.audit.models import AuditLog, AuditLogArchive
from apps.audit.serializers import AuditLogArchiveSerializer, AuditLogSerializer
from apps.audit.selectors import AuditLogSelector
from common.permissions import IsActiveUser, IsSuperAdmin


class AuditLogListView(generics.ListAPIView):
    """List audit logs."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogSerializer
    filterset_fields = ["action", "entity_type", "user"]
    search_fields = ["user_email", "entity_type", "description", "reason"]
    ordering_fields = ["timestamp", "action"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        """Get audit log queryset."""
        return AuditLog.objects.all()


class AuditLogDetailView(generics.RetrieveAPIView):
    """Retrieve audit log details."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get audit log queryset."""
        return AuditLog.objects.all()


class AuditLogByUserView(generics.ListAPIView):
    """List audit logs for a specific user."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogSerializer
    ordering = ["-timestamp"]

    def get_queryset(self):
        """Get user's audit logs."""
        user_id = self.kwargs.get("user_id")
        selector = AuditLogSelector()
        return selector.get_by_user(user_id)


class AuditLogByEntityView(generics.ListAPIView):
    """List audit logs for a specific entity."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogSerializer
    ordering = ["-timestamp"]

    def get_queryset(self):
        """Get entity's audit logs."""
        entity_type = self.kwargs.get("entity_type")
        entity_id = self.kwargs.get("entity_id")
        selector = AuditLogSelector()
        return selector.get_by_entity(entity_type, entity_id)


class AuditLogRecentView(generics.ListAPIView):
    """List recent audit logs."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogSerializer
    ordering = ["-timestamp"]

    def get_queryset(self):
        """Get recent audit logs."""
        days = int(self.kwargs.get("days", 7))
        selector = AuditLogSelector()
        return selector.get_recent_logs(days)


class AuditLogArchiveListView(generics.ListAPIView):
    """List archived audit logs."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsSuperAdmin]
    serializer_class = AuditLogArchiveSerializer
    ordering = ["-original_timestamp"]

    def get_queryset(self):
        """Get archived audit logs."""
        return AuditLogArchive.objects.all()
