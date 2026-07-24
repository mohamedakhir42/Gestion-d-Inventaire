"""
Custom permissions for accounts app.
"""

from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from apps.accounts.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission to allow access to owner or admin users."""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """Check if user is owner or admin."""
        if request.user.is_superuser or request.user.is_admin():
            return True
        return obj == request.user


class IsSameRoleOrHigher(permissions.BasePermission):
    """Permission to allow access to same role or higher."""

    ROLE_HIERARCHY = {
        User.Role.SUPER_ADMIN: 7,
        User.Role.ADMINISTRATOR: 6,
        User.Role.WAREHOUSE_MANAGER: 5,
        User.Role.MAINTENANCE_MANAGER: 5,
        User.Role.WAREHOUSE_OPERATOR: 4,
        User.Role.TECHNICIAN: 3,
        User.Role.VIEWER: 1,
    }

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """Check if user has same or higher role."""
        if request.user.is_superuser:
            return True

        user_level = self.ROLE_HIERARCHY.get(request.user.role, 0)
        target_level = self.ROLE_HIERARCHY.get(obj.role, 0)

        return user_level >= target_level


class CanManageUsers(permissions.BasePermission):
    """Permission to manage users."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user can manage users."""
        return request.user and request.user.is_authenticated and request.user.is_admin()

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """Check if user can manage specific user."""
        if request.user.is_superuser:
            return True
        if request.user.role == User.Role.SUPER_ADMIN:
            return obj.role != User.Role.SUPER_ADMIN
        if request.user.role == User.Role.ADMINISTRATOR:
            return obj.role in [User.Role.VIEWER, User.Role.WAREHOUSE_OPERATOR, User.Role.TECHNICIAN]
        return False


class CanInviteUsers(permissions.BasePermission):
    """Permission to invite users."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user can invite users."""
        return request.user and request.user.is_authenticated and request.user.is_admin()
