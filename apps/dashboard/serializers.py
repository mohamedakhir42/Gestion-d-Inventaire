"""
Serializers for dashboard app.
"""

from rest_framework import serializers


class OverviewStatsSerializer(serializers.Serializer):
    """Serializer for overview statistics."""

    total_products = serializers.IntegerField()
    total_warehouses = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(max_digits=14, decimal_places=2)
    low_stock_items = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    today_movements = serializers.IntegerField()


class StockByWarehouseSerializer(serializers.Serializer):
    """Serializer for stock by warehouse."""

    code = serializers.CharField()
    name = serializers.CharField()
    total_quantity = serializers.DecimalField(max_digits=12, decimal_places=3)
    total_value = serializers.DecimalField(max_digits=14, decimal_places=2)


class MovementStatsSerializer(serializers.Serializer):
    """Serializer for movement statistics."""

    total_movements = serializers.IntegerField()
    by_type = serializers.ListField()
    by_status = serializers.ListField()


class TopProductSerializer(serializers.Serializer):
    """Serializer for top products."""

    product__internal_code = serializers.CharField()
    product__name = serializers.CharField()
    total_quantity = serializers.DecimalField(max_digits=12, decimal_places=3)


class RequestStatsSerializer(serializers.Serializer):
    """Serializer for request statistics."""

    total_requests = serializers.IntegerField()
    by_status = serializers.ListField()
    by_priority = serializers.ListField()
    avg_completion_time = serializers.FloatField()


class WarehouseUtilizationSerializer(serializers.Serializer):
    """Serializer for warehouse utilization."""

    warehouse_code = serializers.CharField()
    warehouse_name = serializers.CharField()
    total_capacity = serializers.DecimalField(max_digits=12, decimal_places=2)
    used_capacity = serializers.DecimalField(max_digits=12, decimal_places=2)
    utilization_percentage = serializers.FloatField()


class CategoryDistributionSerializer(serializers.Serializer):
    """Serializer for category distribution."""

    name = serializers.CharField()
    code = serializers.CharField()
    product_count = serializers.IntegerField()
    total_stock = serializers.DecimalField(max_digits=12, decimal_places=3)


class RecentActivitySerializer(serializers.Serializer):
    """Serializer for recent activity."""

    action = serializers.CharField()
    entity_type = serializers.CharField()
    user_email = serializers.EmailField()
    timestamp = serializers.DateTimeField()
    description = serializers.CharField(allow_blank=True)


class ReportSerializer(serializers.Serializer):
    """Serializer for reports."""

    report_type = serializers.CharField()
    generated_at = serializers.DateTimeField()
