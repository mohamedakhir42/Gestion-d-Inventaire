"""
Business logic services for audit app.
"""

from typing import Any

from apps.audit.models import AuditLog, AuditLogArchive
from common.services import BaseService


class AuditService(BaseService):
    """Service for audit log management."""

    model = AuditLog

    def log_create(
        self,
        user: Any,
        entity_type: str,
        entity_id: Any,
        new_data: dict,
        request: Any = None,
        description: str = None,
    ) -> AuditLog:
        """Log a create action."""
        return AuditLog.log_action(
            action=AuditLog.Action.CREATE,
            user=user,
            entity_type=entity_type,
            entity_id=entity_id,
            new_data=new_data,
            request=request,
            description=description,
        )

    def log_update(
        self,
        user: Any,
        entity_type: str,
        entity_id: Any,
        old_data: dict,
        new_data: dict,
        changed_fields: list,
        request: Any = None,
        description: str = None,
    ) -> AuditLog:
        """Log an update action."""
        return AuditLog.log_action(
            action=AuditLog.Action.UPDATE,
            user=user,
            entity_type=entity_type,
            entity_id=entity_id,
            old_data=old_data,
            new_data=new_data,
            changed_fields=changed_fields,
            request=request,
            description=description,
        )

    def log_delete(
        self,
        user: Any,
        entity_type: str,
        entity_id: Any,
        old_data: dict,
        request: Any = None,
        description: str = None,
        reason: str = None,
    ) -> AuditLog:
        """Log a delete action."""
        return AuditLog.log_action(
            action=AuditLog.Action.DELETE,
            user=user,
            entity_type=entity_type,
            entity_id=entity_id,
            old_data=old_data,
            request=request,
            description=description,
            reason=reason,
        )

    def log_login(self, user: Any, request: Any = None) -> AuditLog:
        """Log a login action."""
        return AuditLog.log_action(
            action=AuditLog.Action.LOGIN,
            user=user,
            entity_type="User",
            entity_id=user.id,
            request=request,
            description=f"User logged in: {user.email}",
        )

    def log_logout(self, user: Any, request: Any = None) -> AuditLog:
        """Log a logout action."""
        return AuditLog.log_action(
            action=AuditLog.Action.LOGOUT,
            user=user,
            entity_type="User",
            entity_id=user.id,
            request=request,
            description=f"User logged out: {user.email}",
        )

    def log_password_reset(self, user: Any, request: Any = None) -> AuditLog:
        """Log a password reset action."""
        return AuditLog.log_action(
            action=AuditLog.Action.PASSWORD_RESET,
            user=user,
            entity_type="User",
            entity_id=user.id,
            request=request,
            description=f"Password reset for: {user.email}",
        )

    def archive_old_logs(self, days: int = 90) -> int:
        """Archive audit logs older than specified days."""
        from django.utils import timezone

        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        old_logs = AuditLog.objects.filter(timestamp__lt=cutoff_date)

        archived_count = 0
        for log in old_logs:
            AuditLogArchive.objects.create(
                user_email=log.user_email,
                user_role=log.user_role,
                action=log.action,
                entity_type=log.entity_type,
                entity_id=log.entity_id,
                old_data=log.old_data,
                new_data=log.new_data,
                changed_fields=log.changed_fields,
                ip_address=log.ip_address,
                user_agent=log.user_agent,
                description=log.description,
                reason=log.reason,
                original_timestamp=log.timestamp,
            )
            log.delete()
            archived_count += 1

        return archived_count
