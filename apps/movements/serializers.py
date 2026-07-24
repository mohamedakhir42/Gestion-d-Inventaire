"""
Serializers for movements app.
"""

from rest_framework import serializers

from apps.movements.models import Movement, StockRequest, StockRequestItem


class MovementSerializer(serializers.ModelSerializer):
    """Serializer for Movement model."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.internal_code", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    warehouse_code = serializers.CharField(source="warehouse.code", read_only=True)
    from_location_name = serializers.CharField(source="from_location.get_full_location", read_only=True)
    to_location_name = serializers.CharField(source="to_location.get_full_location", read_only=True)
    type_display = serializers.CharField(source="get_movement_type_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    requested_by_name = serializers.CharField(source="requested_by.get_full_name", read_only=True)
    approved_by_name = serializers.CharField(source="approved_by.get_full_name", read_only=True)
    validated_by_name = serializers.CharField(source="validated_by.get_full_name", read_only=True)
    performed_by_name = serializers.CharField(source="performed_by.get_full_name", read_only=True)

    class Meta:
        model = Movement
        fields = [
            "id",
            "movement_type",
            "type_display",
            "status",
            "status_display",
            "reference_number",
            "product",
            "product_name",
            "product_code",
            "warehouse",
            "warehouse_name",
            "warehouse_code",
            "from_location",
            "from_location_name",
            "to_location",
            "to_location_name",
            "from_warehouse",
            "to_warehouse",
            "quantity",
            "unit_cost",
            "total_cost",
            "reason",
            "comment",
            "requested_by",
            "requested_by_name",
            "approved_by",
            "approved_by_name",
            "approved_at",
            "validated_by",
            "validated_by_name",
            "validated_at",
            "performed_by",
            "performed_by_name",
            "performed_at",
            "movement_date",
            "expected_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reference_number",
            "approved_at",
            "validated_at",
            "performed_at",
            "movement_date",
            "created_at",
            "updated_at",
        ]


class MovementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating movements."""

    class Meta:
        model = Movement
        fields = [
            "movement_type",
            "product",
            "warehouse",
            "from_location",
            "to_location",
            "from_warehouse",
            "to_warehouse",
            "quantity",
            "unit_cost",
            "reason",
            "comment",
            "expected_date",
        ]


class StockRequestItemSerializer(serializers.ModelSerializer):
    """Serializer for StockRequestItem model."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.internal_code", read_only=True)
    unit_symbol = serializers.CharField(source="unit.symbol", read_only=True)

    class Meta:
        model = StockRequestItem
        fields = [
            "id",
            "stock_request",
            "product",
            "product_name",
            "product_code",
            "quantity",
            "unit",
            "unit_symbol",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class StockRequestSerializer(serializers.ModelSerializer):
    """Serializer for StockRequest model."""

    items = StockRequestItemSerializer(many=True, read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    warehouse_code = serializers.CharField(source="warehouse.code", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    requested_by_name = serializers.CharField(source="requested_by.get_full_name", read_only=True)
    approved_by_name = serializers.CharField(source="approved_by.get_full_name", read_only=True)
    rejected_by_name = serializers.CharField(source="rejected_by.get_full_name", read_only=True)
    validated_by_name = serializers.CharField(source="validated_by.get_full_name", read_only=True)

    class Meta:
        model = StockRequest
        fields = [
            "id",
            "reference_number",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "title",
            "description",
            "warehouse",
            "warehouse_name",
            "warehouse_code",
            "items",
            "requested_by",
            "requested_by_name",
            "requested_at",
            "approved_by",
            "approved_by_name",
            "approved_at",
            "rejected_by",
            "rejected_by_name",
            "rejected_at",
            "rejection_reason",
            "validated_by",
            "validated_by_name",
            "validated_at",
            "required_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reference_number",
            "requested_at",
            "approved_at",
            "rejected_at",
            "validated_at",
            "created_at",
            "updated_at",
        ]


class StockRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating stock requests."""

    items = StockRequestItemSerializer(many=True)

    class Meta:
        model = StockRequest
        fields = [
            "title",
            "description",
            "warehouse",
            "priority",
            "required_by",
            "items",
        ]

    def create(self, validated_data):
        """Create stock request with items."""
        items_data = validated_data.pop("items")
        stock_request = StockRequest.objects.create(**validated_data)
        for item_data in items_data:
            StockRequestItem.objects.create(stock_request=stock_request, **item_data)
        return stock_request
