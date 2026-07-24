"""
Categories app configuration.
"""

from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """Categories app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.categories"
    verbose_name = "Categories"
