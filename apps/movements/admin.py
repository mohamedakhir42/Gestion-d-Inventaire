"""
Admin configuration for movements app.
"""

from django.contrib import admin

from apps.movements.models import Movement, StockRequest, StockRequestItem


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    """Admin interface for Movement model."""

    list_display = [
        "reference_number",
        "movement_type",
        "status",
        "product",
        "warehouse",
        "quantity",
        "requested_by",
        "movement_date",
        "created_at",
    ]
    list_filter = ["movement_type", "status", "warehouse", "movement_date"]
    search_fields = ["reference_number", "product__name", "product__internal_code"]
    ordering = ["-movement_date"]
    readonly_fields = [
        "reference_number",
        "approved_at",
        "validated_at",
        "performed_at",
        "movement_date",
        "created_at",
        "updated_at",
    ]


class StockRequestItemInline(admin.TabularInline):
    """Inline for StockRequestItem."""

    model = StockRequestItem
    extra = 1
    readonly_fields = ["created_at", "updated_at"]


@admin.register(StockRequest)
class StockRequestAdmin(admin.ModelAdmin):
    """Admin interface for StockRequest model."""

    list_display = [
        "reference_number",
        "title",
        "status",
        "priority",
        "warehouse",
        "requested_by",
        "requested_at",
        "required_by",
    ]
    list_filter = ["status", "priority", "warehouse", "requested_at"]
    search_fields = ["title", "reference_number"]
    ordering = ["-requested_at"]
    readonly_fields = [
        "reference_number",
        "requested_at",
        "approved_at",
        "rejected_at",
        "validated_at",
        "created_at",
        "updated_at",
    ]
    inlines = [StockRequestItemInline]


@admin.register(StockRequestItem)
class StockRequestItemAdmin(admin.ModelAdmin):
    """Admin interface for StockRequestItem model."""

    list_display = ["stock_request", "product", "quantity", "unit", "created_at"]
    list_filter = ["stock_request", "unit", "created_at"]
    search_fields = ["product__name", "product__internal_code"]
    ordering = ["stock_request", "product"]
