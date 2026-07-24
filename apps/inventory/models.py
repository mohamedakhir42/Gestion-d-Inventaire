"""
Inventory models including products, brands, and units.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from common.validators import BarcodeValidator, InternalCodeValidator


class Brand(BaseModel):
    """Brand model for product brands."""

    name = models.CharField(_("brand name"), max_length=100, unique=True)
    code = models.CharField(_("brand code"), max_length=20, unique=True, db_index=True)
    description = models.TextField(_("description"), blank=True)
    website = models.URLField(_("website"), blank=True)
    logo = models.ImageField(_("logo"), upload_to="brands/", blank=True, null=True)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name}"


class Unit(BaseModel):
    """Unit of measurement model."""

    name = models.CharField(_("unit name"), max_length=50, unique=True)
    code = models.CharField(_("unit code"), max_length=10, unique=True, db_index=True)
    symbol = models.CharField(_("symbol"), max_length=10, unique=True)
    description = models.TextField(_("description"), blank=True)
    is_base_unit = models.BooleanField(_("is base unit"), default=False)
    conversion_factor = models.DecimalField(
        _("conversion factor"),
        max_digits=10,
        decimal_places=4,
        default=1.0,
        help_text=_("Conversion factor to base unit"),
    )
    base_unit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="derived_units",
    )
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("unit")
        verbose_name_plural = _("units")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name} ({self.symbol})"


class Product(BaseModel):
    """Product model for inventory items."""

    class Status(models.TextChoices):
        """Product status."""

        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        DISCONTINUED = "DISCONTINUED", _("Discontinued")

    # Identification
    internal_code = models.CharField(
        _("internal code"),
        max_length=30,
        unique=True,
        validators=[InternalCodeValidator()],
        db_index=True,
    )
    barcode = models.CharField(
        _("barcode"),
        max_length=20,
        unique=True,
        validators=[BarcodeValidator()],
        db_index=True,
    )
    qr_code = models.CharField(_("QR code"), max_length=100, unique=True, blank=True, db_index=True)
    name = models.CharField(_("product name"), max_length=200)
    description = models.TextField(_("description"), blank=True)

    # Classification
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="products",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="products",
    )

    # Supplier
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="products",
    )

    # Pricing
    purchase_price = models.DecimalField(_("purchase price"), max_digits=12, decimal_places=2)
    average_cost = models.DecimalField(_("average cost"), max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(_("selling price"), max_digits=12, decimal_places=2, null=True, blank=True)

    # Stock thresholds
    minimum_stock = models.DecimalField(_("minimum stock"), max_digits=12, decimal_places=3, default=0)
    maximum_stock = models.DecimalField(_("maximum stock"), max_digits=12, decimal_places=3, default=0)

    # Current stock (calculated from stock movements)
    current_stock = models.DecimalField(_("current stock"), max_digits=12, decimal_places=3, default=0)
    reserved_stock = models.DecimalField(_("reserved stock"), max_digits=12, decimal_places=3, default=0)
    available_stock = models.DecimalField(_("available stock"), max_digits=12, decimal_places=3, default=0)

    # Media
    image = models.ImageField(_("product image"), upload_to="products/", blank=True, null=True)
    specifications = models.JSONField(_("specifications"), default=dict, blank=True)

    # Status
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.ACTIVE)

    # Tracking
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_products",
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_products",
    )

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["internal_code"]
        indexes = [
            models.Index(fields=["internal_code"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["qr_code"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.internal_code} - {self.name}"

    def calculate_available_stock(self) -> None:
        """Calculate available stock."""
        self.available_stock = self.current_stock - self.reserved_stock
        self.save(update_fields=["available_stock"])

    def is_below_minimum(self) -> bool:
        """Check if stock is below minimum."""
        return self.current_stock < self.minimum_stock

    def is_above_maximum(self) -> bool:
        """Check if stock is above maximum."""
        return self.current_stock > self.maximum_stock
