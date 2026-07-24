"""
Custom permissions for movements app.
"""

from rest_framework import permissions

from common.permissions import IsMaintenanceManager, IsWarehouseManager


class CanApproveRequests(permissions.BasePermission):
    """Permission to approve stock requests."""

    def has_permission(self, request, view):
        """Check if user can approve requests."""
        return request.user and request.user.is_authenticated and request.user.is_maintenance_manager()


class CanValidateMovements(permissions.BasePermission):
    """Permission to validate movements."""

    def has_permission(self, request, view):
        """Check if user can validate movements."""
        return request.user and request.user.is_authenticated and request.user.is_warehouse_manager()


class CanCreateMovements(permissions.BasePermission):
    """Permission to create movements."""

    def has_permission(self, request, view):
        """Check if user can create movements."""
        return request.user and request.user.is_authenticated and request.user.is_warehouse_manager()
