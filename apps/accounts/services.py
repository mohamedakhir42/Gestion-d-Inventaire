"""
Business logic services for accounts app.
"""

import logging
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import LoginHistory, User
from common.services import BaseService
from common.utils import get_client_ip

logger = logging.getLogger(__name__)

User = get_user_model()


class AuthService(BaseService):
    """Service for authentication operations."""

    model = User

    def create_login_history(self, user: User, request: Any, status: str = "SUCCESS") -> LoginHistory:
        """Create login history entry."""
        return LoginHistory.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            status=status,
        )

    def logout_user(self, user: User, request: Any) -> None:
        """Handle user logout."""
        try:
            login_history = LoginHistory.objects.filter(user=user, logout_time__isnull=True).latest("login_time")
            login_history.logout_time = timezone.now()
            login_history.save()
        except LoginHistory.DoesNotExist:
            pass


class UserService(BaseService):
    """Service for user management operations."""

    model = User

    def invite_user(self, data: dict, inviter: User) -> User:
        """Invite a new user."""
        user = self.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data.get("phone", ""),
            employee_id=data["employee_id"],
            department=data.get("department", ""),
            position=data.get("position", ""),
            role=data.get("role", User.Role.VIEWER),
            created_by=inviter,
            updated_by=inviter,
        )
        user.regenerate_invitation_token()
        logger.info(f"User invited: {user.email} by {inviter.email}")
        return user

    def activate_user(self, token: str, password: str, avatar: Optional[Any] = None) -> User:
        """Activate user account with password and avatar."""
        user = self.get_queryset().get(invitation_token=token, status=User.Status.PENDING)
        user.set_password(password)
        user.activate_account()
        if avatar:
            user.avatar = avatar
        user.save()
        logger.info(f"User activated: {user.email}")
        return user

    def reset_password(self, user: User, new_password: str) -> None:
        """Reset user password."""
        user.set_password(new_password)
        user.save()
        logger.info(f"Password reset for user: {user.email}")

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        """Change user password with old password verification."""
        if not user.check_password(old_password):
            raise ValueError(_("Old password is incorrect."))
        user.set_password(new_password)
        user.save()
        logger.info(f"Password changed for user: {user.email}")

    def resend_invitation(self, user: User) -> str:
        """Resend invitation to user."""
        if user.status != User.Status.PENDING:
            raise ValueError(_("Cannot resend invitation for non-pending user."))
        token = user.regenerate_invitation_token()
        logger.info(f"Invitation resent to: {user.email}")
        return token

    def deactivate_user(self, user: User, admin: User) -> None:
        """Deactivate user account."""
        user.deactivate_account()
        user.updated_by = admin
        user.save()
        logger.info(f"User deactivated: {user.email} by {admin.email}")

    def suspend_user(self, user: User, admin: User) -> None:
        """Suspend user account."""
        user.suspend_account()
        user.updated_by = admin
        user.save()
        logger.info(f"User suspended: {user.email} by {admin.email}")

    def restore_user(self, user: User, admin: User) -> None:
        """Restore suspended or deactivated user."""
        user.status = User.Status.ACTIVE
        user.is_active = True
        user.updated_by = admin
        user.save()
        logger.info(f"User restored: {user.email} by {admin.email}")


class PermissionService(BaseService):
    """Service for permission management."""

    def grant_permission_to_role(self, role: str, permission_codename: str) -> Any:
        """Grant permission to a role."""
        from apps.accounts.models import Permission, RolePermission

        permission = Permission.objects.get(codename=permission_codename)
        role_permission, created = RolePermission.objects.get_or_create(
            role=role,
            permission=permission,
        )
        return role_permission

    def revoke_permission_from_role(self, role: str, permission_codename: str) -> None:
        """Revoke permission from a role."""
        from apps.accounts.models import Permission, RolePermission

        permission = Permission.objects.get(codename=permission_codename)
        RolePermission.objects.filter(role=role, permission=permission).delete()

    def get_user_permissions(self, user: User) -> list[str]:
        """Get all permissions for a user based on their role."""
        from apps.accounts.models import RolePermission

        role_permissions = RolePermission.objects.filter(role=user.role).select_related("permission")
        return [rp.permission.codename for rp in role_permissions]

    def user_has_permission(self, user: User, permission_codename: str) -> bool:
        """Check if user has specific permission."""
        if user.is_superuser:
            return True
        return permission_codename in self.get_user_permissions(user)
