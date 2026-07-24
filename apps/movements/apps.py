"""
Movements app configuration.
"""

from django.apps import AppConfig


class MovementsConfig(AppConfig):
    """Movements app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.movements"
    verbose_name = "Stock Movements"
