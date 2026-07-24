"""
Admin configuration for warehouses app.
"""

from django.contrib import admin

from apps.warehouses.models import Bin, Row, Shelf, Warehouse, Zone


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Admin interface for Warehouse model."""

    list_display = ["code", "name", "city", "country", "manager", "status", "created_at"]
    list_filter = ["status", "country", "created_at"]
    search_fields = ["name", "code", "address"]
    ordering = ["code"]


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    """Admin interface for Zone model."""

    list_display = ["code", "name", "warehouse", "zone_type", "is_active", "created_at"]
    list_filter = ["zone_type", "is_active", "warehouse", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["warehouse", "code"]


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    """Admin interface for Row model."""

    list_display = ["code", "name", "zone", "is_active", "created_at"]
    list_filter = ["is_active", "zone", "created_at"]
    search_fields = ["name", "code"]
    ordering = ["zone", "code"]


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    """Admin interface for Shelf model."""

    list_display = ["code", "name", "row", "height", "weight_limit", "is_active", "created_at"]
    list_filter = ["is_active", "row", "created_at"]
    search_fields = ["name", "code"]
    ordering = ["row", "code"]


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    """Admin interface for Bin model."""

    list_display = ["code", "name", "shelf", "capacity", "used_capacity", "is_active", "created_at"]
    list_filter = ["is_active", "shelf", "created_at"]
    search_fields = ["name", "code"]
    ordering = ["shelf", "code"]
