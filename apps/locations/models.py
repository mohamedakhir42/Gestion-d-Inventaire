"""
Location models for product storage locations.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class ProductLocation(BaseModel):
    """Product location model linking products to storage locations."""

    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.CASCADE,
        related_name="locations",
    )
    warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.CASCADE,
        related_name="product_locations",
    )
    zone = models.ForeignKey(
        "warehouses.Zone",
        on_delete=models.CASCADE,
        related_name="product_locations",
        null=True,
        blank=True,
    )
    row = models.ForeignKey(
        "warehouses.Row",
        on_delete=models.CASCADE,
        related_name="product_locations",
        null=True,
        blank=True,
    )
    shelf = models.ForeignKey(
        "warehouses.Shelf",
        on_delete=models.CASCADE,
        related_name="product_locations",
        null=True,
        blank=True,
    )
    bin = models.ForeignKey(
        "warehouses.Bin",
        on_delete=models.CASCADE,
        related_name="product_locations",
        null=True,
        blank=True,
    )
    quantity = models.DecimalField(_("quantity"), max_digits=12, decimal_places=3, default=0)
    is_primary = models.BooleanField(_("is primary location"), default=False)

    class Meta:
        verbose_name = _("product location")
        verbose_name_plural = _("product locations")
        ordering = ["product", "warehouse"]
        unique_together = ["product", "warehouse", "bin"]
        indexes = [
            models.Index(fields=["product", "warehouse"]),
            models.Index(fields=["bin"]),
            models.Index(fields=["is_primary"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        location = self.bin or self.shelf or self.row or self.zone or self.warehouse
        return f"{self.product.internal_code} - {location}"

    def get_full_location(self) -> str:
        """Get full location path."""
        if self.bin:
            return self.bin.get_full_location()
        elif self.shelf:
            return f"{self.shelf.row.zone.warehouse.code} > {self.shelf.row.zone.code} > {self.shelf.row.code} > {self.shelf.code}"
        elif self.row:
            return f"{self.row.zone.warehouse.code} > {self.row.zone.code} > {self.row.code}"
        elif self.zone:
            return f"{self.zone.warehouse.code} > {self.zone.code}"
        else:
            return self.warehouse.code
