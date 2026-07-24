"""
Tests for movements app.
"""

import pytest
from rest_framework.test import APIClient

from apps.movements.models import Movement, StockRequest
from apps.inventory.models import Product
from apps.categories.models import Category
from apps.warehouses.models import Warehouse
from apps.accounts.models import User


@pytest.mark.django_db
class TestMovementModel:
    """Test Movement model."""

    def test_create_movement(self):
        """Test creating a movement."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        category = Category.objects.create(name="Electronics", code="ELEC")
        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            purchase_price=100.00,
        )
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )

        movement = Movement.objects.create(
            movement_type=Movement.Type.ENTRY,
            product=product,
            warehouse=warehouse,
            quantity=50,
            reason="Initial stock",
            requested_by=user,
        )

        assert movement.movement_type == Movement.Type.ENTRY
        assert movement.quantity == 50
        assert movement.status == Movement.Status.PENDING

    def test_approve_movement(self):
        """Test approving a movement."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        category = Category.objects.create(name="Electronics", code="ELEC")
        product = Product.objects.create(
            internal_code="PRD001",
            barcode="1234567890123",
            name="Test Product",
            category=category,
            purchase_price=100.00,
        )
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )

        movement = Movement.objects.create(
            movement_type=Movement.Type.ENTRY,
            product=product,
            warehouse=warehouse,
            quantity=50,
            reason="Initial stock",
            requested_by=user,
        )

        movement.approve(user)
        assert movement.status == Movement.Status.APPROVED
        assert movement.approved_by == user


@pytest.mark.django_db
class TestStockRequestModel:
    """Test StockRequest model."""

    def test_create_stock_request(self):
        """Test creating a stock request."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )

        request = StockRequest.objects.create(
            title="Test Request",
            description="Need materials",
            warehouse=warehouse,
            requested_by=user,
            priority=StockRequest.Priority.MEDIUM,
        )

        assert request.title == "Test Request"
        assert request.status == StockRequest.Status.PENDING

    def test_approve_request(self):
        """Test approving a stock request."""
        warehouse = Warehouse.objects.create(code="WH001", name="Warehouse 1", address="Address", city="City", country="Country", postal_code="12345")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )

        request = StockRequest.objects.create(
            title="Test Request",
            description="Need materials",
            warehouse=warehouse,
            requested_by=user,
            priority=StockRequest.Priority.MEDIUM,
        )

        request.approve(user)
        assert request.status == StockRequest.Status.APPROVED
        assert request.approved_by == user
