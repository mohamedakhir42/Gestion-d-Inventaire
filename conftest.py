"""
Pytest configuration for the project.
"""

import pytest
from django.conf import settings
from django.test.utils import get_runner


@pytest.fixture(scope="function")
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup database for tests."""
    pass


@pytest.fixture
def api_client():
    """Return an API client."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_user(api_client):
    """Create and authenticate a test user."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
        employee_id="EMP001",
    )
    user.activate_account()

    # Login and get token
    response = api_client.post(
        "/api/auth/login/",
        {"email": "test@example.com", "password": "testpass123"},
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return user
