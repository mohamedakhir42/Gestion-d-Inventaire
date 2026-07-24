"""
API views for notifications app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from common.permissions import IsActiveUser


class NotificationListView(generics.ListAPIView):
    """List notifications."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = NotificationSerializer
    filterset_fields = ["notification_type", "status", "recipient"]
    search_fields = ["subject", "recipient_email"]
    ordering_fields = ["created_at", "sent_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get notification queryset."""
        return Notification.objects.filter(is_deleted=False)


class NotificationDetailView(generics.RetrieveAPIView):
    """Retrieve notification details."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = NotificationSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get notification queryset."""
        return Notification.objects.filter(is_deleted=False)


class MyNotificationsView(generics.ListAPIView):
    """List current user's notifications."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = NotificationSerializer
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get user's notifications."""
        return Notification.objects.filter(recipient=self.request.user, is_deleted=False)
