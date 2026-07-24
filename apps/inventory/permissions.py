"""
Custom permissions for inventory app.
"""

from rest_framework import permissions

from common.permissions import IsWarehouseManager, IsWarehouseOperator


class CanManageProducts(permissions.BasePermission):
    """Permission to manage products."""

    def has_permission(self, request, view):
        """Check if user can manage products."""
        return request.user and request.user.is_authenticated and request.user.is_warehouse_manager()


class CanViewProducts(permissions.BasePermission):
    """Permission to view products."""

    def has_permission(self, request, view):
        """Check if user can view products."""
        return request.user and request.user.is_authenticated
