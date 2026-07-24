"""
Suppliers app configuration.
"""

from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    """Suppliers app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.suppliers"
    verbose_name = "Suppliers"
