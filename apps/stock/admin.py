"""
Admin configuration for stock app.
"""

from django.contrib import admin

from apps.stock.models import Stock, StockReservation


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Admin interface for Stock model."""

    list_display = [
        "product",
        "warehouse",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "minimum_level",
        "reorder_level",
        "variance",
        "created_at",
    ]
    list_filter = ["warehouse", "created_at"]
    search_fields = ["product__name", "product__internal_code"]
    ordering = ["product", "warehouse"]
    readonly_fields = ["available_quantity", "variance", "created_at", "updated_at"]


@admin.register(StockReservation)
class StockReservationAdmin(admin.ModelAdmin):
    """Admin interface for StockReservation model."""

    list_display = [
        "reference_number",
        "stock",
        "quantity",
        "status",
        "reserved_by",
        "reserved_until",
        "created_at",
    ]
    list_filter = ["status", "reserved_until", "created_at"]
    search_fields = ["reference_number", "stock__product__name"]
    ordering = ["-created_at"]
