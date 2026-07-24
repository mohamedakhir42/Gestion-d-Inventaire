"""
Stock app configuration.
"""

from django.apps import AppConfig


class StockConfig(AppConfig):
    """Stock app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.stock"
    verbose_name = "Stock"
