"""
Warehouses app configuration.
"""

from django.apps import AppConfig


class WarehousesConfig(AppConfig):
    """Warehouses app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.warehouses"
    verbose_name = "Warehouses"
