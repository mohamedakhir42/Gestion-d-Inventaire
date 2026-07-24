"""
Data selectors for accounts app.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Q

from common.selectors import BaseSelector

User = get_user_model()


class UserSelector(BaseSelector):
    """Selector for User model."""

    model = User

    def get_active_users(self) -> Any:
        """Get all active users."""
        return self.filter(status=User.Status.ACTIVE, is_active=True)

    def get_by_email(self, email: str) -> User:
        """Get user by email."""
        return self.get_queryset().get(email=email)

    def get_by_employee_id(self, employee_id: str) -> User:
        """Get user by employee ID."""
        return self.get_queryset().get(employee_id=employee_id)

    def search_users(self, query: str) -> Any:
        """Search users by name or email."""
        return self.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(employee_id__icontains=query)
        )

    def get_by_role(self, role: str) -> Any:
        """Get users by role."""
        return self.filter(role=role)

    def get_pending_users(self) -> Any:
        """Get pending users."""
        return self.filter(status=User.Status.PENDING)

    def get_by_invitation_token(self, token: str) -> User:
        """Get user by invitation token."""
        return self.get_queryset().get(invitation_token=token)


class LoginHistorySelector(BaseSelector):
    """Selector for LoginHistory model."""

    from apps.accounts.models import LoginHistory

    model = LoginHistory

    def get_user_login_history(self, user: User) -> Any:
        """Get login history for a user."""
        return self.filter(user=user)

    def get_recent_logins(self, days: int = 30) -> Any:
        """Get recent logins within specified days."""
        from django.utils import timezone

        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(login_time__gte=since)
