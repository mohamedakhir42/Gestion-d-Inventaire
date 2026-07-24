"""
Admin configuration for inventory app.
"""

from django.contrib import admin

from apps.inventory.models import Brand, Product, Unit


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin interface for Brand model."""

    list_display = ["code", "name", "website", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Admin interface for Unit model."""

    list_display = ["code", "name", "symbol", "is_base_unit", "is_active", "created_at"]
    list_filter = ["is_base_unit", "is_active", "created_at"]
    search_fields = ["name", "code", "symbol"]
    ordering = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = [
        "internal_code",
        "name",
        "category",
        "brand",
        "supplier",
        "current_stock",
        "available_stock",
        "status",
        "created_at",
    ]
    list_filter = ["status", "category", "brand", "supplier", "created_at"]
    search_fields = ["name", "internal_code", "barcode", "description"]
    ordering = ["internal_code"]
    readonly_fields = ["current_stock", "reserved_stock", "available_stock", "created_at", "updated_at"]
