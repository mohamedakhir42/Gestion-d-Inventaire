"""
Supplier models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from common.validators import PhoneValidator


class Supplier(BaseModel):
    """Supplier model for managing product suppliers."""

    class Status(models.TextChoices):
        """Supplier status."""

        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        BLOCKED = "BLOCKED", _("Blocked")

    code = models.CharField(_("supplier code"), max_length=20, unique=True, db_index=True)
    name = models.CharField(_("company name"), max_length=200)
    contact_person = models.CharField(_("contact person"), max_length=100)
    email = models.EmailField(_("email"), db_index=True)
    phone = models.CharField(_("phone"), max_length=20, validators=[PhoneValidator()])
    address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=100)
    country = models.CharField(_("country"), max_length=100)
    tax_id = models.CharField(_("tax ID"), max_length=50, blank=True)
    website = models.URLField(_("website"), blank=True)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    payment_terms = models.CharField(_("payment terms"), max_length=100, blank=True)
    notes = models.TextField(_("notes"), blank=True)
    rating = models.DecimalField(_("rating"), max_digits=3, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("supplier")
        verbose_name_plural = _("suppliers")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["email"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name}"
