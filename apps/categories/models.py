"""
Category and subcategory models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Category(BaseModel):
    """Category model for product classification."""

    name = models.CharField(_("name"), max_length=100, unique=True)
    code = models.CharField(_("code"), max_length=20, unique=True, db_index=True)
    description = models.TextField(_("description"), blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    image = models.ImageField(_("image"), upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name}"

    def get_full_path(self) -> str:
        """Get full category path including parents."""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name

    def get_all_children(self) -> models.QuerySet:
        """Get all children categories recursively."""
        children = list(self.children.all())
        for child in children:
            children.extend(child.get_all_children())
        return children
