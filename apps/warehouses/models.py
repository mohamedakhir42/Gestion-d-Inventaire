"""
Warehouse models with zones, rows, shelves, and bins.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Warehouse(BaseModel):
    """Warehouse model for storage locations."""

    class Status(models.TextChoices):
        """Warehouse status."""

        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        MAINTENANCE = "MAINTENANCE", _("Maintenance")

    code = models.CharField(_("warehouse code"), max_length=20, unique=True, db_index=True)
    name = models.CharField(_("warehouse name"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=100)
    country = models.CharField(_("country"), max_length=100)
    postal_code = models.CharField(_("postal code"), max_length=20)
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    email = models.EmailField(_("email"), blank=True)
    manager = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_warehouses",
    )
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.ACTIVE)
    capacity = models.DecimalField(_("capacity"), max_digits=12, decimal_places=2, null=True, blank=True)
    area = models.DecimalField(_("area"), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_("Area in square meters"))
    temperature_min = models.DecimalField(_("min temperature"), max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_max = models.DecimalField(_("max temperature"), max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_min = models.DecimalField(_("min humidity"), max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_max = models.DecimalField(_("max humidity"), max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("warehouse")
        verbose_name_plural = _("warehouses")
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["status"]),
            models.Index(fields=["manager"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.code} - {self.name}"

    def get_total_capacity(self) -> float:
        """Get total capacity from all zones."""
        return sum(zone.capacity or 0 for zone in self.zones.all())

    def get_used_capacity(self) -> float:
        """Get used capacity from all zones."""
        return sum(zone.used_capacity or 0 for zone in self.zones.all())


class Zone(BaseModel):
    """Zone model for warehouse zones."""

    class Type(models.TextChoices):
        """Zone types."""

        STORAGE = "STORAGE", _("Storage")
        RECEIVING = "RECEIVING", _("Receiving")
        SHIPPING = "SHIPPING", _("Shipping")
        QUALITY_CONTROL = "QUALITY_CONTROL", _("Quality Control")
        COLD_STORAGE = "COLD_STORAGE", _("Cold Storage")
        HAZARDOUS = "HAZARDOUS", _("Hazardous")

    code = models.CharField(_("zone code"), max_length=20, db_index=True)
    name = models.CharField(_("zone name"), max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="zones")
    zone_type = models.CharField(_("zone type"), max_length=30, choices=Type.choices, default=Type.STORAGE)
    description = models.TextField(_("description"), blank=True)
    capacity = models.DecimalField(_("capacity"), max_digits=12, decimal_places=2, null=True, blank=True)
    used_capacity = models.DecimalField(_("used capacity"), max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("zone")
        verbose_name_plural = _("zones")
        ordering = ["warehouse", "code"]
        unique_together = ["warehouse", "code"]
        indexes = [
            models.Index(fields=["warehouse", "code"]),
            models.Index(fields=["zone_type"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.warehouse.code} - {self.code} - {self.name}"

    def get_available_capacity(self) -> float:
        """Get available capacity."""
        return (self.capacity or 0) - self.used_capacity

    def get_utilization_percentage(self) -> float:
        """Get utilization percentage."""
        if self.capacity and self.capacity > 0:
            return (self.used_capacity / self.capacity) * 100
        return 0


class Row(BaseModel):
    """Row model for warehouse rows."""

    code = models.CharField(_("row code"), max_length=20, db_index=True)
    name = models.CharField(_("row name"), max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="rows")
    description = models.TextField(_("description"), blank=True)
    capacity = models.DecimalField(_("capacity"), max_digits=12, decimal_places=2, null=True, blank=True)
    used_capacity = models.DecimalField(_("used capacity"), max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("row")
        verbose_name_plural = _("rows")
        ordering = ["zone", "code"]
        unique_together = ["zone", "code"]
        indexes = [
            models.Index(fields=["zone", "code"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.zone.code} - {self.code} - {self.name}"


class Shelf(BaseModel):
    """Shelf model for warehouse shelves."""

    code = models.CharField(_("shelf code"), max_length=20, db_index=True)
    name = models.CharField(_("shelf name"), max_length=100)
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="shelves")
    description = models.TextField(_("description"), blank=True)
    capacity = models.DecimalField(_("capacity"), max_digits=12, decimal_places=2, null=True, blank=True)
    used_capacity = models.DecimalField(_("used capacity"), max_digits=12, decimal_places=2, default=0)
    height = models.DecimalField(_("height"), max_digits=6, decimal_places=2, null=True, blank=True)
    weight_limit = models.DecimalField(_("weight limit"), max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("shelf")
        verbose_name_plural = _("shelves")
        ordering = ["row", "code"]
        unique_together = ["row", "code"]
        indexes = [
            models.Index(fields=["row", "code"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.row.code} - {self.code} - {self.name}"


class Bin(BaseModel):
    """Bin model for warehouse bins."""

    code = models.CharField(_("bin code"), max_length=20, db_index=True)
    name = models.CharField(_("bin name"), max_length=100)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name="bins")
    description = models.TextField(_("description"), blank=True)
    capacity = models.DecimalField(_("capacity"), max_digits=12, decimal_places=2, null=True, blank=True)
    used_capacity = models.DecimalField(_("used capacity"), max_digits=12, decimal_places=2, default=0)
    length = models.DecimalField(_("length"), max_digits=6, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(_("width"), max_digits=6, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(_("depth"), max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("bin")
        verbose_name_plural = _("bins")
        ordering = ["shelf", "code"]
        unique_together = ["shelf", "code"]
        indexes = [
            models.Index(fields=["shelf", "code"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.shelf.code} - {self.code} - {self.name}"

    def get_full_location(self) -> str:
        """Get full location path."""
        return f"{self.shelf.row.zone.warehouse.code} > {self.shelf.row.zone.code} > {self.shelf.row.code} > {self.shelf.code} > {self.code}"

    def get_available_capacity(self) -> float:
        """Get available capacity."""
        return (self.capacity or 0) - self.used_capacity
