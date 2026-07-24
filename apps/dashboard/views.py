"""
API views for dashboard app.
"""

from datetime import datetime

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.dashboard.serializers import (
    CategoryDistributionSerializer,
    MovementStatsSerializer,
    OverviewStatsSerializer,
    RecentActivitySerializer,
    RequestStatsSerializer,
    StockByWarehouseSerializer,
    TopProductSerializer,
    WarehouseUtilizationSerializer,
)
from apps.dashboard.services import DashboardService, ReportService
from common.permissions import IsActiveUser


class DashboardViewSet(ViewSet):
    """ViewSet for dashboard analytics."""

    permission_classes = [IsAuthenticated, IsActiveUser]

    def __init__(self, **kwargs):
        """Initialize viewset with services."""
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService()
        self.report_service = ReportService()

    def list(self, request):
        """Get dashboard overview."""
        stats = self.dashboard_service.get_overview_stats()
        serializer = OverviewStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stock_by_warehouse(self, request):
        """Get stock distribution by warehouse."""
        data = self.dashboard_service.get_stock_by_warehouse()
        serializer = StockByWarehouseSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def movement_stats(self, request):
        """Get movement statistics."""
        days = int(request.query_params.get("days", 30))
        stats = self.dashboard_service.get_movement_stats(days)
        serializer = MovementStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_products(self, request):
        """Get top products by movement."""
        limit = int(request.query_params.get("limit", 10))
        data = self.dashboard_service.get_top_products(limit)
        serializer = TopProductSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def request_stats(self, request):
        """Get request statistics."""
        days = int(request.query_params.get("days", 30))
        stats = self.dashboard_service.get_request_stats(days)
        serializer = RequestStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def warehouse_utilization(self, request):
        """Get warehouse utilization statistics."""
        data = self.dashboard_service.get_warehouse_utilization()
        serializer = WarehouseUtilizationSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def category_distribution(self, request):
        """Get category distribution."""
        data = self.dashboard_service.get_category_distribution()
        serializer = CategoryDistributionSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent_activity(self, request):
        """Get recent activity."""
        limit = int(request.query_params.get("limit", 20))
        data = self.dashboard_service.get_recent_activity(limit)
        serializer = RecentActivitySerializer(data, many=True)
        return Response(serializer.data)


class ReportViewSet(ViewSet):
    """ViewSet for generating reports."""

    permission_classes = [IsAuthenticated, IsActiveUser]

    def __init__(self, **kwargs):
        """Initialize viewset with report service."""
        super().__init__(**kwargs)
        self.report_service = ReportService()

    @action(detail=False, methods=["get"])
    def inventory(self, request):
        """Generate inventory report."""
        warehouse_id = request.query_params.get("warehouse_id")
        report = self.report_service.generate_inventory_report(warehouse_id)
        return Response(report)

    @action(detail=False, methods=["get"])
    def movement(self, request):
        """Generate movement report."""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        warehouse_id = request.query_params.get("warehouse_id")

        if not start_date or not end_date:
            return Response(
                {"error": "start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = self.report_service.generate_movement_report(start_date, end_date, warehouse_id)
        return Response(report)

    @action(detail=False, methods=["get"])
    def request(self, request):
        """Generate stock request report."""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = self.report_service.generate_request_report(start_date, end_date)
        return Response(report)
