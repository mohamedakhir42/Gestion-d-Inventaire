"""
Inventory app configuration.
"""

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """Inventory app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.inventory"
    verbose_name = "Inventory"
