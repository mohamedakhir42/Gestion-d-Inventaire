"""
Admin configuration for suppliers app.
"""

from django.contrib import admin

from apps.suppliers.models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin interface for Supplier model."""

    list_display = ["code", "name", "contact_person", "email", "status", "rating", "created_at"]
    list_filter = ["status", "country", "created_at"]
    search_fields = ["name", "code", "contact_person", "email"]
    ordering = ["name"]
