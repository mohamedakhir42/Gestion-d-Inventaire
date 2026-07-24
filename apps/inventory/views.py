"""
API views for inventory app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.inventory.models import Brand, Product, Unit
from apps.inventory.serializers import (
    BrandSerializer,
    ProductCreateSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
    UnitSerializer,
)
from apps.inventory.services import BrandService, ProductService, UnitService
from apps.inventory.selectors import BrandSelector, ProductSelector, UnitSelector
from common.mixins import AuditMixin
from common.permissions import IsActiveUser


class BrandListView(generics.ListCreateAPIView):
    """List and create brands."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = BrandSerializer
    filterset_fields = ["is_active"]
    search_fields = ["name", "code"]
    ordering = ["name"]

    def get_queryset(self):
        """Get brand queryset."""
        return Brand.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        """Create brand with service."""
        service = BrandService()
        service.create_brand(serializer.validated_data)


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a brand."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = BrandSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get brand queryset."""
        return Brand.objects.filter(is_deleted=False)


class UnitListView(generics.ListCreateAPIView):
    """List and create units."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = UnitSerializer
    filterset_fields = ["is_active", "is_base_unit"]
    search_fields = ["name", "code", "symbol"]
    ordering = ["name"]

    def get_queryset(self):
        """Get unit queryset."""
        return Unit.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        """Create unit with service."""
        service = UnitService()
        service.create_unit(serializer.validated_data)


class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a unit."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = UnitSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get unit queryset."""
        return Unit.objects.filter(is_deleted=False)


class ProductListView(generics.ListCreateAPIView):
    """List and create products."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ProductSerializer
    filterset_fields = ["category", "brand", "supplier", "unit", "status"]
    search_fields = ["name", "internal_code", "barcode", "description"]
    ordering_fields = ["name", "internal_code", "current_stock", "created_at"]
    ordering = ["internal_code"]

    def get_queryset(self):
        """Get product queryset."""
        return Product.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        """Create product with service."""
        service = ProductService()
        service.create_product(serializer.validated_data, self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a product."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get product queryset."""
        return Product.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.request.method in ["PUT", "PATCH"]:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_update(self, serializer):
        """Update product with audit."""
        serializer.save(updated_by=self.request.user)


class ProductByBarcodeView(generics.RetrieveAPIView):
    """Retrieve product by barcode."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ProductSerializer
    lookup_field = "barcode"

    def get_queryset(self):
        """Get product queryset."""
        return Product.objects.filter(is_deleted=False)
