"""
Tests for inventory app.
"""

import pytest
from rest_framework.test import APIClient

from apps.inventory.models import Product, Brand, Unit
from apps.categories.models import Category
from apps.suppliers.models import Supplier
from apps.accounts.models import User


@pytest.mark.django_db
class TestProductModel:
    """Test Product model."""

    def test_create_product(self):
        """Test creating a product."""
        category = Category.objects.create(name="Electronics", code="ELEC")
        brand = Brand.objects.create(name="BrandX", code="BRX")
        unit = Unit.objects.create(name="Piece", code="PC", symbol="pc")
        supplier = Supplier.objects.create(
            code="SUP001",
            name="Supplier X",
            contact_person="John Doe",
            email="john@supplier.com",
            phone="+1234567890",
            address="123 Street",
            city="City",
            country="Country",
        )
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )

        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            brand=brand,
            unit=unit,
            supplier=supplier,
            purchase_price=100.00,
            created_by=user,
        )

        assert product.internal_code == "PRD001"
        assert product.name == "Test Product"
        assert product.current_stock == 0

    def test_product_is_below_minimum(self):
        """Test is_below_minimum method."""
        category = Category.objects.create(name="Electronics", code="ELEC")
        brand = Brand.objects.create(name="BrandX", code="BRX")
        unit = Unit.objects.create(name="Piece", code="PC", symbol="pc")
        supplier = Supplier.objects.create(
            code="SUP001",
            name="Supplier X",
            contact_person="John Doe",
            email="john@supplier.com",
            phone="+1234567890",
            address="123 Street",
            city="City",
            country="Country",
        )

        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            brand=brand,
            unit=unit,
            supplier=supplier,
            purchase_price=100.00,
            minimum_stock=10,
            current_stock=5,
        )

        assert product.is_below_minimum()


@pytest.mark.django_db
class TestProductAPI:
    """Test Product API endpoints."""

    def test_list_products(self):
        """Test listing products."""
        client = APIClient()
        response = client.get("/api/inventory/products/")
        assert response.status_code == 200

    def test_create_product_unauthorized(self):
        """Test creating product without authentication."""
        client = APIClient()
        response = client.post(
            "/api/inventory/products/",
            {
                "internal_code": "PRD001",
                "barcode": "1234567890123",
                "name": "Test Product",
            },
        )
        assert response.status_code == 401
