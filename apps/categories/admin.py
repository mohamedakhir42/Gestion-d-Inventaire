"""
Admin configuration for categories app.
"""

from django.contrib import admin

from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ["code", "name", "parent", "is_active", "created_at"]
    list_filter = ["is_active", "parent", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]
    prepopulated_fields = {"code": ("name",)}
