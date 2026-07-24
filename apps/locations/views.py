"""
API views for locations app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.locations.models import ProductLocation
from apps.locations.serializers import ProductLocationSerializer
from common.permissions import IsActiveUser


class ProductLocationListView(generics.ListCreateAPIView):
    """List and create product locations."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ProductLocationSerializer
    filterset_fields = ["product", "warehouse", "zone", "row", "shelf", "bin", "is_primary"]
    ordering = ["product", "warehouse"]

    def get_queryset(self):
        """Get product location queryset."""
        return ProductLocation.objects.filter(is_deleted=False)


class ProductLocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product location."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ProductLocationSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get product location queryset."""
        return ProductLocation.objects.filter(is_deleted=False)
