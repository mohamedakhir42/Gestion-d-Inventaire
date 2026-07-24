"""
Serializers for stock app.
"""

from rest_framework import serializers

from apps.stock.models import Stock, StockReservation


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.internal_code", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    warehouse_code = serializers.CharField(source="warehouse.code", read_only=True)
    is_below_minimum = serializers.BooleanField(source="is_below_minimum", read_only=True)
    is_below_reorder = serializers.BooleanField(source="is_below_reorder", read_only=True)
    is_above_maximum = serializers.BooleanField(source="is_above_maximum", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id",
            "product",
            "product_name",
            "product_code",
            "warehouse",
            "warehouse_name",
            "warehouse_code",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "minimum_level",
            "maximum_level",
            "reorder_level",
            "reorder_quantity",
            "last_count_date",
            "last_count_quantity",
            "variance",
            "is_below_minimum",
            "is_below_reorder",
            "is_above_maximum",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class StockReservationSerializer(serializers.ModelSerializer):
    """Serializer for StockReservation model."""

    stock_product = serializers.CharField(source="stock.product.internal_code", read_only=True)
    stock_warehouse = serializers.CharField(source="stock.warehouse.code", read_only=True)
    reserved_by_name = serializers.CharField(source="reserved_by.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = StockReservation
        fields = [
            "id",
            "stock",
            "stock_product",
            "stock_warehouse",
            "reference_number",
            "quantity",
            "status",
            "status_display",
            "reserved_by",
            "reserved_by_name",
            "reserved_until",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class StockCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating stock."""

    class Meta:
        model = Stock
        fields = [
            "product",
            "warehouse",
            "quantity",
            "reserved_quantity",
            "minimum_level",
            "maximum_level",
            "reorder_level",
            "reorder_quantity",
        ]


class StockUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating stock."""

    class Meta:
        model = Stock
        fields = [
            "minimum_level",
            "maximum_level",
            "reorder_level",
            "reorder_quantity",
            "last_count_date",
            "last_count_quantity",
        ]
