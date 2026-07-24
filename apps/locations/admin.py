"""
Admin configuration for locations app.
"""

from django.contrib import admin

from apps.locations.models import ProductLocation


@admin.register(ProductLocation)
class ProductLocationAdmin(admin.ModelAdmin):
    """Admin interface for ProductLocation model."""

    list_display = ["product", "warehouse", "bin", "quantity", "is_primary", "created_at"]
    list_filter = ["warehouse", "is_primary", "created_at"]
    search_fields = ["product__name", "product__internal_code"]
    ordering = ["product", "warehouse"]
