"""
Data selectors for audit app.
"""

from datetime import datetime, timedelta

from django.db.models import Q

from common.selectors import BaseSelector

from apps.audit.models import AuditLog


class AuditLogSelector(BaseSelector):
    """Selector for AuditLog model."""

    model = AuditLog

    def get_by_user(self, user_id):
        """Get logs by user."""
        return self.filter(user_id=user_id)

    def get_by_action(self, action: str):
        """Get logs by action type."""
        return self.filter(action=action)

    def get_by_entity(self, entity_type: str, entity_id):
        """Get logs by entity."""
        return self.filter(entity_type=entity_type, entity_id=entity_id)

    def get_by_date_range(self, start_date: datetime, end_date: datetime):
        """Get logs within date range."""
        return self.filter(timestamp__range=[start_date, end_date])

    def get_recent_logs(self, days: int = 7):
        """Get logs from recent days."""
        since = datetime.now() - timedelta(days=days)
        return self.filter(timestamp__gte=since)

    def get_by_ip_address(self, ip_address: str):
        """Get logs by IP address."""
        return self.filter(ip_address=ip_address)

    def search_logs(self, query: str):
        """Search logs by various fields."""
        return self.filter(
            Q(user_email__icontains=query)
            | Q(entity_type__icontains=query)
            | Q(description__icontains=query)
            | Q(reason__icontains=query)
        )

    def get_failed_attempts(self, user_id=None):
        """Get failed login attempts or suspicious activity."""
        queryset = self.filter(action__in=[AuditLog.Action.PASSWORD_RESET])
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
