"""
Stock movement models for tracking inventory movements.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Movement(BaseModel):
    """Movement model for tracking stock movements."""

    class Type(models.TextChoices):
        """Movement types."""

        ENTRY = "ENTRY", _("Entry")
        EXIT = "EXIT", _("Exit")
        TRANSFER = "TRANSFER", _("Transfer")
        ADJUSTMENT = "ADJUSTMENT", _("Adjustment")
        INVENTORY_CORRECTION = "INVENTORY_CORRECTION", _("Inventory Correction")
        RETURN = "RETURN", _("Return")
        DAMAGE = "DAMAGE", _("Damage")
        LOSS = "LOSS", _("Loss")
        CONSUMPTION = "CONSUMPTION", _("Consumption")

    class Status(models.TextChoices):
        """Movement status."""

        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        VALIDATED = "VALIDATED", _("Validated")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")

    movement_type = models.CharField(_("movement type"), max_length=30, choices=Type.choices)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    reference_number = models.CharField(_("reference number"), max_length=50, unique=True, db_index=True)

    # Product and location
    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.PROTECT,
        related_name="movements",
    )
    warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.PROTECT,
        related_name="movements",
    )
    from_location = models.ForeignKey(
        "warehouses.Bin",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements_from",
    )
    to_location = models.ForeignKey(
        "warehouses.Bin",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements_to",
    )

    # For transfers
    from_warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements_from",
    )
    to_warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movements_to",
    )

    # Quantity and details
    quantity = models.DecimalField(_("quantity"), max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(_("unit cost"), max_digits=12, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(_("total cost"), max_digits=14, decimal_places=2, null=True, blank=True)

    # Reason and comments
    reason = models.TextField(_("reason"))
    comment = models.TextField(_("comment"), blank=True)

    # Workflow tracking
    requested_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="requested_movements",
    )
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_movements",
    )
    approved_at = models.DateTimeField(_("approved at"), null=True, blank=True)
    validated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_movements",
    )
    validated_at = models.DateTimeField(_("validated at"), null=True, blank=True)
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="performed_movements",
    )
    performed_at = models.DateTimeField(_("performed at"), null=True, blank=True)

    # Dates
    movement_date = models.DateTimeField(_("movement date"), auto_now_add=True)
    expected_date = models.DateTimeField(_("expected date"), null=True, blank=True)

    class Meta:
        verbose_name = _("movement")
        verbose_name_plural = _("movements")
        ordering = ["-movement_date"]
        indexes = [
            models.Index(fields=["reference_number"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["product"]),
            models.Index(fields=["warehouse"]),
            models.Index(fields=["movement_date"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.reference_number} - {self.movement_type} - {self.product.internal_code}"

    def approve(self, user) -> None:
        """Approve the movement."""
        from django.utils import timezone

        self.status = self.Status.APPROVED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def validate(self, user) -> None:
        """Validate the movement."""
        from django.utils import timezone

        self.status = self.Status.VALIDATED
        self.validated_by = user
        self.validated_at = timezone.now()
        self.save()

    def complete(self, user) -> None:
        """Complete the movement and update stock."""
        from django.utils import timezone

        self.status = self.Status.COMPLETED
        self.performed_by = user
        self.performed_at = timezone.now()
        self.save()

        # Update stock
        from apps.stock.models import Stock
        from apps.stock.services import StockService

        try:
            stock = Stock.objects.get(product=self.product, warehouse=self.warehouse)
            service = StockService()
            service.update_stock_quantity(stock, float(self.quantity), self.movement_type)
        except Stock.DoesNotExist:
            # Create stock record if it doesn't exist
            from apps.stock.models import Stock

            stock = Stock.objects.create(
                product=self.product,
                warehouse=self.warehouse,
                quantity=float(self.quantity),
            )
            stock.calculate_available_quantity()

    def cancel(self, user) -> None:
        """Cancel the movement."""
        self.status = self.Status.CANCELLED
        self.save()


class StockRequest(BaseModel):
    """Stock request model for technician request workflow."""

    class Status(models.TextChoices):
        """Request status."""

        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")
        VALIDATED = "VALIDATED", _("Validated")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")

    class Priority(models.TextChoices):
        """Request priority."""

        LOW = "LOW", _("Low")
        MEDIUM = "MEDIUM", _("Medium")
        HIGH = "HIGH", _("High")
        URGENT = "URGENT", _("Urgent")

    reference_number = models.CharField(_("reference number"), max_length=50, unique=True, db_index=True)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(_("priority"), max_length=20, choices=Priority.choices, default=Priority.MEDIUM)

    # Request details
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    warehouse = models.ForeignKey(
        "warehouses.Warehouse",
        on_delete=models.PROTECT,
        related_name="stock_requests",
    )

    # Workflow tracking
    requested_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="stock_requests",
    )
    requested_at = models.DateTimeField(_("requested at"), auto_now_add=True)
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_requests",
    )
    approved_at = models.DateTimeField(_("approved at"), null=True, blank=True)
    rejected_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_requests",
    )
    rejected_at = models.DateTimeField(_("rejected at"), null=True, blank=True)
    rejection_reason = models.TextField(_("rejection reason"), blank=True)
    validated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_requests",
    )
    validated_at = models.DateTimeField(_("validated at"), null=True, blank=True)

    # Dates
    required_by = models.DateField(_("required by"), null=True, blank=True)

    class Meta:
        verbose_name = _("stock request")
        verbose_name_plural = _("stock requests")
        ordering = ["-requested_at"]
        indexes = [
            models.Index(fields=["reference_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["warehouse"]),
            models.Index(fields=["requested_at"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.reference_number} - {self.title}"

    def approve(self, user) -> None:
        """Approve the request."""
        from django.utils import timezone

        self.status = self.Status.APPROVED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def reject(self, user, reason: str) -> None:
        """Reject the request."""
        from django.utils import timezone

        self.status = self.Status.REJECTED
        self.rejected_by = user
        self.rejected_at = timezone.now()
        self.rejection_reason = reason
        self.save()

    def validate(self, user) -> None:
        """Validate the request."""
        from django.utils import timezone

        self.status = self.Status.VALIDATED
        self.validated_by = user
        self.validated_at = timezone.now()
        self.save()

    def complete(self) -> None:
        """Complete the request."""
        self.status = self.Status.COMPLETED
        self.save()

    def cancel(self) -> None:
        """Cancel the request."""
        self.status = self.Status.CANCELLED
        self.save()


class StockRequestItem(BaseModel):
    """Stock request item model for individual items in a request."""

    stock_request = models.ForeignKey(StockRequest, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.PROTECT,
        related_name="request_items",
    )
    quantity = models.DecimalField(_("quantity"), max_digits=12, decimal_places=3)
    unit = models.ForeignKey(
        "inventory.Unit",
        on_delete=models.PROTECT,
        related_name="request_items",
    )
    notes = models.TextField(_("notes"), blank=True)

    class Meta:
        verbose_name = _("stock request item")
        verbose_name_plural = _("stock request items")
        ordering = ["stock_request", "product"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.stock_request.reference_number} - {self.product.internal_code}: {self.quantity}"
