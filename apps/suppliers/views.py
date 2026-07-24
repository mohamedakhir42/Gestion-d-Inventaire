"""
API views for suppliers app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.suppliers.models import Supplier
from apps.suppliers.serializers import SupplierSerializer
from common.permissions import IsActiveUser


class SupplierListView(generics.ListCreateAPIView):
    """List and create suppliers."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = SupplierSerializer
    filterset_fields = ["status", "city", "country"]
    search_fields = ["name", "code", "contact_person", "email"]
    ordering_fields = ["name", "code", "rating", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        """Get supplier queryset."""
        return Supplier.objects.filter(is_deleted=False)


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a supplier."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = SupplierSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get supplier queryset."""
        return Supplier.objects.filter(is_deleted=False)
