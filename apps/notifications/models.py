"""
Notification models for tracking sent notifications.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Notification(BaseModel):
    """Notification model for tracking sent notifications."""

    class Type(models.TextChoices):
        """Notification types."""

        INVITATION = "INVITATION", _("Invitation")
        PASSWORD_RESET = "PASSWORD_RESET", _("Password Reset")
        LOW_STOCK = "LOW_STOCK", _("Low Stock")
        REQUEST_APPROVED = "REQUEST_APPROVED", _("Request Approved")
        REQUEST_REJECTED = "REQUEST_REJECTED", _("Request Rejected")
        SYSTEM = "SYSTEM", _("System")

    class Status(models.TextChoices):
        """Notification status."""

        PENDING = "PENDING", _("Pending")
        SENT = "SENT", _("Sent")
        FAILED = "FAILED", _("Failed")

    recipient = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="notifications",
    )
    recipient_email = models.EmailField(_("recipient email"))
    notification_type = models.CharField(_("notification type"), max_length=30, choices=Type.choices)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    subject = models.CharField(_("subject"), max_length=255)
    body = models.TextField(_("body"))
    data = models.JSONField(_("data"), null=True, blank=True)
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    error_message = models.TextField(_("error message"), blank=True)

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient"]),
            models.Index(fields=["notification_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.notification_type} - {self.recipient_email}"

    def mark_as_sent(self) -> None:
        """Mark notification as sent."""
        from django.utils import timezone

        self.status = self.Status.SENT
        self.sent_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message: str) -> None:
        """Mark notification as failed."""
        self.status = self.Status.FAILED
        self.error_message = error_message
        self.save()
