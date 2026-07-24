"""
API views for stock app.
"""

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.stock.models import Stock, StockReservation
from apps.stock.serializers import (
    StockCreateSerializer,
    StockReservationSerializer,
    StockSerializer,
    StockUpdateSerializer,
)
from apps.stock.services import StockReservationService, StockService
from apps.stock.selectors import StockReservationSelector, StockSelector
from common.permissions import IsActiveUser, IsWarehouseManager


class StockViewSet(ModelViewSet):
    """ViewSet for Stock model."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    filterset_fields = ["warehouse", "product"]
    search_fields = ["product__name", "product__internal_code"]
    ordering_fields = ["quantity", "available_quantity", "created_at"]
    ordering = ["product"]

    def get_queryset(self):
        """Get stock queryset."""
        return Stock.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.action == "create":
            return StockCreateSerializer
        if self.action in ["update", "partial_update"]:
            return StockUpdateSerializer
        return StockSerializer

    def perform_create(self, serializer):
        """Create stock with service."""
        service = StockService()
        service.create_stock(serializer.validated_data)

    @action(detail=True, methods=["post"])
    def count(self, request, pk=None):
        """Perform stock count."""
        stock = self.get_object()
        counted_quantity = request.data.get("counted_quantity")
        if counted_quantity is None:
            return Response({"error": "counted_quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = StockService()
        service.perform_stock_count(stock, float(counted_quantity))

        return Response({"detail": "Stock count recorded successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Get low stock items."""
        selector = StockSelector()
        queryset = selector.get_low_stock()
        page = self.paginate_queryset(queryset)
        serializer = StockSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def reorder_stock(self, request):
        """Get items needing reorder."""
        selector = StockSelector()
        queryset = selector.get_reorder_stock()
        page = self.paginate_queryset(queryset)
        serializer = StockSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class StockReservationViewSet(ModelViewSet):
    """ViewSet for StockReservation model."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = StockReservationSerializer
    filterset_fields = ["stock", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get reservation queryset."""
        return StockReservation.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        """Create reservation with service."""
        service = StockReservationService()
        service.create_reservation(serializer.validated_data, self.request.user)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        """Confirm reservation."""
        reservation = self.get_object()
        service = StockReservationService()
        service.confirm_reservation(reservation)
        return Response({"detail": "Reservation confirmed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel reservation."""
        reservation = self.get_object()
        service = StockReservationService()
        service.cancel_reservation(reservation)
        return Response({"detail": "Reservation cancelled successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def fulfill(self, request, pk=None):
        """Fulfill reservation."""
        reservation = self.get_object()
        service = StockReservationService()
        service.fulfill_reservation(reservation)
        return Response({"detail": "Reservation fulfilled successfully."}, status=status.HTTP_200_OK)
