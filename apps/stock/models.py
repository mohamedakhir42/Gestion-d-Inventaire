"""
Stock models for inventory stock management.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Stock(BaseModel):
    """Stock model for tracking product inventory."""

    product = models.OneToOneField(
        "inventory.Product",
        on_delete=models.CASCADE,
        related_name="stock",
    )
    warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    quantity = models.DecimalField(_("quantity"), max_digits=12, decimal_places=3, default=0)
    reserved_quantity = models.DecimalField(_("reserved quantity"), max_digits=12, decimal_places=3, default=0)
    available_quantity = models.DecimalField(_("available quantity"), max_digits=12, decimal_places=3, default=0)
    minimum_level = models.DecimalField(_("minimum level"), max_digits=12, decimal_places=3, default=0)
    maximum_level = models.DecimalField(_("maximum level"), max_digits=12, decimal_places=3, default=0)
    reorder_level = models.DecimalField(_("reorder level"), max_digits=12, decimal_places=3, default=0)
    reorder_quantity = models.DecimalField(_("reorder quantity"), max_digits=12, decimal_places=3, default=0)
    last_count_date = models.DateField(_("last count date"), null=True, blank=True)
    last_count_quantity = models.DecimalField(_("last count quantity"), max_digits=12, decimal_places=3, default=0)
    variance = models.DecimalField(_("variance"), max_digits=12, decimal_places=3, default=0)

    class Meta:
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")
        ordering = ["product", "warehouse"]
        unique_together = ["product", "warehouse"]
        indexes = [
            models.Index(fields=["product", "warehouse"]),
            models.Index(fields=["warehouse"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.product.internal_code} - {self.warehouse.code}: {self.quantity}"

    def calculate_available_quantity(self) -> None:
        """Calculate available quantity."""
        self.available_quantity = self.quantity - self.reserved_quantity
        self.save(update_fields=["available_quantity"])

    def is_below_minimum(self) -> bool:
        """Check if stock is below minimum level."""
        return self.quantity < self.minimum_level

    def is_below_reorder(self) -> bool:
        """Check if stock is below reorder level."""
        return self.quantity < self.reorder_level

    def is_above_maximum(self) -> bool:
        """Check if stock is above maximum level."""
        return self.quantity > self.maximum_level

    def calculate_variance(self, counted_quantity: float) -> None:
        """Calculate variance between counted and expected quantity."""
        self.variance = counted_quantity - self.quantity
        self.last_count_quantity = counted_quantity
        self.save(update_fields=["variance", "last_count_quantity"])


class StockReservation(BaseModel):
    """Stock reservation model for temporary stock holds."""

    class Status(models.TextChoices):
        """Reservation status."""

        PENDING = "PENDING", _("Pending")
        CONFIRMED = "CONFIRMED", _("Confirmed")
        CANCELLED = "CANCELLED", _("Cancelled")
        FULFILLED = "FULFILLED", _("Fulfilled")

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="reservations")
    reference_number = models.CharField(_("reference number"), max_length=50, unique=True, db_index=True)
    quantity = models.DecimalField(_("quantity"), max_digits=12, decimal_places=3)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    reserved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="stock_reservations",
    )
    reserved_until = models.DateTimeField(_("reserved until"), null=True, blank=True)
    notes = models.TextField(_("notes"), blank=True)

    class Meta:
        verbose_name = _("stock reservation")
        verbose_name_plural = _("stock reservations")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["reference_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["reserved_until"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.reference_number} - {self.stock.product.internal_code}: {self.quantity}"

    def confirm_reservation(self) -> None:
        """Confirm the reservation."""
        self.status = self.Status.CONFIRMED
        self.stock.reserved_quantity += self.quantity
        self.stock.calculate_available_quantity()
        self.save()

    def cancel_reservation(self) -> None:
        """Cancel the reservation."""
        if self.status == self.Status.CONFIRMED:
            self.stock.reserved_quantity -= self.quantity
            self.stock.calculate_available_quantity()
        self.status = self.Status.CANCELLED
        self.save()

    def fulfill_reservation(self) -> None:
        """Fulfill the reservation."""
        if self.status == self.Status.CONFIRMED:
            self.stock.reserved_quantity -= self.quantity
            self.stock.quantity -= self.quantity
            self.stock.calculate_available_quantity()
        self.status = self.Status.FULFILLED
        self.save()
