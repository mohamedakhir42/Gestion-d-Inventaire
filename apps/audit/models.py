"""
Audit log models for tracking system changes.
"""

import uuid
from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class AuditLog(BaseModel):
    """Audit log model for tracking all system changes."""

    class Action(models.TextChoices):
        """Audit action types."""

        CREATE = "CREATE", _("Create")
        UPDATE = "UPDATE", _("Update")
        DELETE = "DELETE", _("Delete")
        LOGIN = "LOGIN", _("Login")
        LOGOUT = "LOGOUT", _("Logout")
        PASSWORD_RESET = "PASSWORD_RESET", _("Password Reset")
        PERMISSION_CHANGE = "PERMISSION_CHANGE", _("Permission Change")
        STOCK_MOVEMENT = "STOCK_MOVEMENT", _("Stock Movement")
        APPROVAL = "APPROVAL", _("Approval")
        REJECTION = "REJECTION", _("Rejection")

    # User information
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs",
    )
    user_email = models.EmailField(_("user email"), blank=True)
    user_role = models.CharField(_("user role"), max_length=30, blank=True)

    # Action information
    action = models.CharField(_("action"), max_length=30, choices=Action.choices)
    entity_type = models.CharField(_("entity type"), max_length=100, blank=True)
    entity_id = models.UUIDField(_("entity ID"), null=True, blank=True)

    # Generic foreign key for related object
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # Data changes
    old_data = models.JSONField(_("old data"), null=True, blank=True)
    new_data = models.JSONField(_("new data"), null=True, blank=True)
    changed_fields = models.JSONField(_("changed fields"), default=list, blank=True)

    # Request information
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    request_method = models.CharField(_("request method"), max_length=10, blank=True)
    request_path = models.CharField(_("request path"), max_length=255, blank=True)

    # Additional context
    description = models.TextField(_("description"), blank=True)
    reason = models.TextField(_("reason"), blank=True)

    # Timestamp
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("audit log")
        verbose_name_plural = _("audit logs")
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["entity_type"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.action} - {self.entity_type} - {self.user_email or 'System'}"

    @classmethod
    def log_action(
        cls,
        action: str,
        user: Any = None,
        entity_type: str = None,
        entity_id: uuid.UUID = None,
        old_data: dict = None,
        new_data: dict = None,
        changed_fields: list = None,
        request: Any = None,
        description: str = None,
        reason: str = None,
        content_object: Any = None,
    ) -> "AuditLog":
        """Create an audit log entry."""
        from common.utils import get_client_ip

        log = cls(
            user=user,
            user_email=user.email if user else None,
            user_role=user.role if user else None,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_data=old_data,
            new_data=new_data,
            changed_fields=changed_fields or [],
            ip_address=get_client_ip(request) if request else None,
            user_agent=request.META.get("HTTP_USER_AGENT", "") if request else None,
            request_method=request.method if request else None,
            request_path=request.path if request else None,
            description=description,
            reason=reason,
        )

        if content_object:
            log.content_object = content_object

        log.save()
        return log


class AuditLogArchive(BaseModel):
    """Archive model for old audit logs."""

    user_email = models.EmailField(_("user email"))
    user_role = models.CharField(_("user role"), max_length=30, blank=True)
    action = models.CharField(_("action"), max_length=30)
    entity_type = models.CharField(_("entity type"), max_length=100, blank=True)
    entity_id = models.UUIDField(_("entity ID"), null=True, blank=True)
    old_data = models.JSONField(_("old data"), null=True, blank=True)
    new_data = models.JSONField(_("new data"), null=True, blank=True)
    changed_fields = models.JSONField(_("changed fields"), default=list, blank=True)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    description = models.TextField(_("description"), blank=True)
    reason = models.TextField(_("reason"), blank=True)
    original_timestamp = models.DateTimeField(_("original timestamp"))
    archived_at = models.DateTimeField(_("archived at"), auto_now_add=True)

    class Meta:
        verbose_name = _("audit log archive")
        verbose_name_plural = _("audit log archives")
        ordering = ["-original_timestamp"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.action} - {self.entity_type} - {self.user_email} (Archived)"
