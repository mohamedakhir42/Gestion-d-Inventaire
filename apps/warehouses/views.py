"""
API views for warehouses app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.warehouses.models import Bin, Row, Shelf, Warehouse, Zone
from apps.warehouses.serializers import (
    BinSerializer,
    RowDetailSerializer,
    RowSerializer,
    ShelfDetailSerializer,
    ShelfSerializer,
    WarehouseDetailSerializer,
    WarehouseSerializer,
    ZoneDetailSerializer,
    ZoneSerializer,
)
from common.permissions import IsActiveUser


class WarehouseListView(generics.ListCreateAPIView):
    """List and create warehouses."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = WarehouseSerializer
    filterset_fields = ["status", "city", "country"]
    search_fields = ["name", "code", "address"]
    ordering_fields = ["name", "code", "created_at"]
    ordering = ["code"]

    def get_queryset(self):
        """Get warehouse queryset."""
        return Warehouse.objects.filter(is_deleted=False)


class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a warehouse."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = WarehouseDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get warehouse queryset."""
        return Warehouse.objects.filter(is_deleted=False)


class ZoneListView(generics.ListCreateAPIView):
    """List and create zones."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ZoneSerializer
    filterset_fields = ["warehouse", "zone_type", "is_active"]
    search_fields = ["name", "code", "description"]
    ordering = ["warehouse", "code"]

    def get_queryset(self):
        """Get zone queryset."""
        warehouse_id = self.kwargs.get("warehouse_id")
        queryset = Zone.objects.filter(is_deleted=False)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
        return queryset


class ZoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a zone."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ZoneDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get zone queryset."""
        return Zone.objects.filter(is_deleted=False)


class RowListView(generics.ListCreateAPIView):
    """List and create rows."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = RowSerializer
    filterset_fields = ["zone", "is_active"]
    search_fields = ["name", "code"]
    ordering = ["zone", "code"]

    def get_queryset(self):
        """Get row queryset."""
        zone_id = self.kwargs.get("zone_id")
        queryset = Row.objects.filter(is_deleted=False)
        if zone_id:
            queryset = queryset.filter(zone_id=zone_id)
        return queryset


class RowDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a row."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = RowDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get row queryset."""
        return Row.objects.filter(is_deleted=False)


class ShelfListView(generics.ListCreateAPIView):
    """List and create shelves."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ShelfSerializer
    filterset_fields = ["row", "is_active"]
    search_fields = ["name", "code"]
    ordering = ["row", "code"]

    def get_queryset(self):
        """Get shelf queryset."""
        row_id = self.kwargs.get("row_id")
        queryset = Shelf.objects.filter(is_deleted=False)
        if row_id:
            queryset = queryset.filter(row_id=row_id)
        return queryset


class ShelfDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a shelf."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = ShelfDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get shelf queryset."""
        return Shelf.objects.filter(is_deleted=False)


class BinListView(generics.ListCreateAPIView):
    """List and create bins."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = BinSerializer
    filterset_fields = ["shelf", "is_active"]
    search_fields = ["name", "code"]
    ordering = ["shelf", "code"]

    def get_queryset(self):
        """Get bin queryset."""
        shelf_id = self.kwargs.get("shelf_id")
        queryset = Bin.objects.filter(is_deleted=False)
        if shelf_id:
            queryset = queryset.filter(shelf_id=shelf_id)
        return queryset


class BinDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a bin."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = BinSerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get bin queryset."""
        return Bin.objects.filter(is_deleted=False)
