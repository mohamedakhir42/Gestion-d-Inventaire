"""
Tests for stock app.
"""

import pytest
from rest_framework.test import APIClient

from apps.stock.models import Stock, StockReservation
from apps.inventory.models import Product
from apps.categories.models import Category
from apps.warehouses.models import Warehouse
from apps.accounts.models import User


@pytest.mark.django_db
class TestStockModel:
    """Test Stock model."""

    def test_create_stock(self):
        """Test creating stock."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        category = Category.objects.create(name="Electronics", code="ELEC")
        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            purchase_price=100.00,
        )

        stock = Stock.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=100,
            minimum_level=10,
        )

        assert stock.quantity == 100
        assert stock.available_quantity == 100

    def test_calculate_available_quantity(self):
        """Test calculating available quantity."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        category = Category.objects.create(name="Electronics", code="ELEC")
        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            purchase_price=100.00,
        )

        stock = Stock.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=100,
            reserved_quantity=20,
            minimum_level=10,
        )

        stock.calculate_available_quantity()
        assert stock.available_quantity == 80

    def test_is_below_minimum(self):
        """Test is_below_minimum method."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        category = Category.objects.create(name="Electronics", code="ELEC")
        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            purchase_price=100.00,
        )

        stock = Stock.objects.create(
            product=product,
            warehouse=warehouse,
            quantity=5,
            minimum_level=10,
        )

        assert stock.is_below_minimum()
