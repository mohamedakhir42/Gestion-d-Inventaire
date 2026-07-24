"""
Custom permission classes.
"""

from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsSuperAdmin(permissions.BasePermission):
    """Permission class for super admin users."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is super admin."""
        return request.user and request.user.is_authenticated and request.user.role == "SUPER_ADMIN"


class IsAdministrator(permissions.BasePermission):
    """Permission class for administrator users."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is administrator."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["SUPER_ADMIN", "ADMINISTRATOR"]
        )


class IsWarehouseManager(permissions.BasePermission):
    """Permission class for warehouse managers."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is warehouse manager."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["SUPER_ADMIN", "ADMINISTRATOR", "WAREHOUSE_MANAGER"]
        )


class IsWarehouseOperator(permissions.BasePermission):
    """Permission class for warehouse operators."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is warehouse operator."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in [
                "SUPER_ADMIN",
                "ADMINISTRATOR",
                "WAREHOUSE_MANAGER",
                "WAREHOUSE_OPERATOR",
            ]
        )


class IsMaintenanceManager(permissions.BasePermission):
    """Permission class for maintenance managers."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is maintenance manager."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in ["SUPER_ADMIN", "ADMINISTRATOR", "MAINTENANCE_MANAGER"]
        )


class IsTechnician(permissions.BasePermission):
    """Permission class for technicians."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is technician."""
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in [
                "SUPER_ADMIN",
                "ADMINISTRATOR",
                "MAINTENANCE_MANAGER",
                "TECHNICIAN",
            ]
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission class for object owners."""

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """Check if user is owner or request is read-only."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class IsActiveUser(permissions.BasePermission):
    """Permission class for active users."""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if user is active."""
        return request.user and request.user.is_authenticated and request.user.is_active
