"""
API views for movements app.
"""

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.movements.models import Movement, StockRequest
from apps.movements.permissions import CanApproveRequests, CanValidateMovements
from apps.movements.serializers import (
    MovementCreateSerializer,
    MovementSerializer,
    StockRequestCreateSerializer,
    StockRequestSerializer,
)
from apps.movements.services import MovementService, StockRequestService
from apps.movements.selectors import MovementSelector, StockRequestSelector
from common.permissions import IsActiveUser, IsMaintenanceManager, IsTechnician, IsWarehouseOperator


class MovementViewSet(ModelViewSet):
    """ViewSet for Movement model."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    filterset_fields = ["movement_type", "status", "warehouse", "product"]
    search_fields = ["reference_number", "product__name", "product__internal_code"]
    ordering_fields = ["movement_date", "reference_number"]
    ordering = ["-movement_date"]

    def get_queryset(self):
        """Get movement queryset."""
        return Movement.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.action == "create":
            return MovementCreateSerializer
        return MovementSerializer

    def perform_create(self, serializer):
        """Create movement with service."""
        service = MovementService()
        service.create_movement(serializer.validated_data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, CanValidateMovements])
    def approve(self, request, pk=None):
        """Approve movement."""
        movement = self.get_object()
        service = MovementService()
        service.approve_movement(movement, request.user)
        return Response({"detail": "Movement approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, CanValidateMovements])
    def validate(self, request, pk=None):
        """Validate movement."""
        movement = self.get_object()
        service = MovementService()
        service.validate_movement(movement, request.user)
        return Response({"detail": "Movement validated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, CanValidateMovements])
    def complete(self, request, pk=None):
        """Complete movement."""
        movement = self.get_object()
        service = MovementService()
        service.complete_movement(movement, request.user)
        return Response({"detail": "Movement completed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel movement."""
        movement = self.get_object()
        service = MovementService()
        service.cancel_movement(movement, request.user)
        return Response({"detail": "Movement cancelled successfully."}, status=status.HTTP_200_OK)


class StockRequestViewSet(ModelViewSet):
    """ViewSet for StockRequest model."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    filterset_fields = ["status", "priority", "warehouse"]
    search_fields = ["title", "reference_number"]
    ordering_fields = ["requested_at", "priority", "required_by"]
    ordering = ["-requested_at"]

    def get_queryset(self):
        """Get request queryset."""
        return StockRequest.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.action == "create":
            return StockRequestCreateSerializer
        return StockRequestSerializer

    def perform_create(self, serializer):
        """Create request with service."""
        service = StockRequestService()
        service.create_request(serializer.validated_data, self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, CanApproveRequests])
    def approve(self, request, pk=None):
        """Approve stock request."""
        stock_request = self.get_object()
        service = StockRequestService()
        service.approve_request(stock_request, request.user)
        return Response({"detail": "Stock request approved successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, CanApproveRequests])
    def reject(self, request, pk=None):
        """Reject stock request."""
        stock_request = self.get_object()
        reason = request.data.get("reason")
        if not reason:
            return Response({"error": "Reason is required for rejection."}, status=status.HTTP_400_BAD_REQUEST)

        service = StockRequestService()
        service.reject_request(stock_request, request.user, reason)
        return Response({"detail": "Stock request rejected successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, IsWarehouseOperator])
    def validate(self, request, pk=None):
        """Validate stock request."""
        stock_request = self.get_object()
        service = StockRequestService()
        service.validate_request(stock_request, request.user)
        return Response({"detail": "Stock request validated successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, IsWarehouseOperator])
    def complete(self, request, pk=None):
        """Complete stock request."""
        stock_request = self.get_object()
        service = StockRequestService()
        service.complete_request(stock_request)
        return Response({"detail": "Stock request completed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel stock request."""
        stock_request = self.get_object()
        service = StockRequestService()
        service.cancel_request(stock_request)
        return Response({"detail": "Stock request cancelled successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsActiveUser, IsWarehouseOperator])
    def create_movements(self, request, pk=None):
        """Create movements from stock request."""
        stock_request = self.get_object()
        if stock_request.status != StockRequest.Status.VALIDATED:
            return Response(
                {"error": "Stock request must be validated before creating movements."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movement_service = MovementService()
        movements = movement_service.create_movement_from_request(stock_request, request.user)

        # Complete the request
        request_service = StockRequestService()
        request_service.complete_request(stock_request)

        return Response(
            {"detail": f"Created {len(movements)} movements from stock request."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def my_requests(self, request):
        """Get current user's requests."""
        selector = StockRequestSelector()
        queryset = selector.get_by_user(request.user)
        page = self.paginate_queryset(queryset)
        serializer = StockRequestSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """Get pending requests."""
        selector = StockRequestSelector()
        queryset = selector.get_pending_requests()
        page = self.paginate_queryset(queryset)
        serializer = StockRequestSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def urgent(self, request):
        """Get urgent requests."""
        selector = StockRequestSelector()
        queryset = selector.get_urgent_requests()
        page = self.paginate_queryset(queryset)
        serializer = StockRequestSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
