"""
Tests for accounts app.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.accounts.models import User, Permission, RolePermission

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")
        assert user.role == User.Role.VIEWER

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
            employee_id="ADM001",
        )
        assert user.is_staff
        assert user.is_superuser
        assert user.role == User.Role.SUPER_ADMIN

    def test_user_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )
        assert user.get_full_name() == "Test User"

    def test_user_has_role(self):
        """Test has_role method."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
            role=User.Role.WAREHOUSE_MANAGER,
        )
        assert user.has_role(User.Role.WAREHOUSE_MANAGER)
        assert not user.has_role(User.Role.ADMINISTRATOR)

    def test_activate_account(self):
        """Test account activation."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )
        user.activate_account()
        assert user.status == User.Status.ACTIVE
        assert user.is_active


@pytest.mark.django_db
class TestAuthenticationAPI:
    """Test authentication API endpoints."""

    def test_login(self):
        """Test user login."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )
        user.activate_account()

        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"email": "test@example.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"email": "test@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_logout(self):
        """Test user logout."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            employee_id="EMP001",
        )
        user.activate_account()

        client = APIClient()
        # Login first
        login_response = client.post(
            "/api/auth/login/",
            {"email": "test@example.com", "password": "testpass123"},
        )
        token = login_response.data["access"]

        # Logout
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.post("/api/auth/logout/")
        assert response.status_code == 200
