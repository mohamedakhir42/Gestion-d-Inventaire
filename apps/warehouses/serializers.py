"""
Serializers for warehouses app.
"""

from rest_framework import serializers

from apps.warehouses.models import Bin, Row, Shelf, Warehouse, Zone


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for Warehouse model."""

    manager_name = serializers.CharField(source="manager.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    total_capacity = serializers.SerializerMethodField()
    used_capacity = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            "id",
            "code",
            "name",
            "description",
            "address",
            "city",
            "country",
            "postal_code",
            "phone",
            "email",
            "manager",
            "manager_name",
            "status",
            "status_display",
            "capacity",
            "area",
            "temperature_min",
            "temperature_max",
            "humidity_min",
            "humidity_max",
            "total_capacity",
            "used_capacity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_total_capacity(self, obj: Warehouse) -> float:
        """Get total capacity."""
        return obj.get_total_capacity()

    def get_used_capacity(self, obj: Warehouse) -> float:
        """Get used capacity."""
        return obj.get_used_capacity()


class ZoneSerializer(serializers.ModelSerializer):
    """Serializer for Zone model."""

    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    warehouse_code = serializers.CharField(source="warehouse.code", read_only=True)
    type_display = serializers.CharField(source="get_zone_type_display", read_only=True)
    available_capacity = serializers.SerializerMethodField()
    utilization_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        fields = [
            "id",
            "code",
            "name",
            "warehouse",
            "warehouse_name",
            "warehouse_code",
            "zone_type",
            "type_display",
            "description",
            "capacity",
            "used_capacity",
            "available_capacity",
            "utilization_percentage",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_available_capacity(self, obj: Zone) -> float:
        """Get available capacity."""
        return obj.get_available_capacity()

    def get_utilization_percentage(self, obj: Zone) -> float:
        """Get utilization percentage."""
        return obj.get_utilization_percentage()


class RowSerializer(serializers.ModelSerializer):
    """Serializer for Row model."""

    zone_name = serializers.CharField(source="zone.name", read_only=True)
    zone_code = serializers.CharField(source="zone.code", read_only=True)
    warehouse_code = serializers.CharField(source="zone.warehouse.code", read_only=True)

    class Meta:
        model = Row
        fields = [
            "id",
            "code",
            "name",
            "zone",
            "zone_name",
            "zone_code",
            "warehouse_code",
            "description",
            "capacity",
            "used_capacity",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ShelfSerializer(serializers.ModelSerializer):
    """Serializer for Shelf model."""

    row_name = serializers.CharField(source="row.name", read_only=True)
    row_code = serializers.CharField(source="row.code", read_only=True)
    zone_code = serializers.CharField(source="row.zone.code", read_only=True)
    warehouse_code = serializers.CharField(source="row.zone.warehouse.code", read_only=True)

    class Meta:
        model = Shelf
        fields = [
            "id",
            "code",
            "name",
            "row",
            "row_name",
            "row_code",
            "zone_code",
            "warehouse_code",
            "description",
            "capacity",
            "used_capacity",
            "height",
            "weight_limit",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class BinSerializer(serializers.ModelSerializer):
    """Serializer for Bin model."""

    shelf_name = serializers.CharField(source="shelf.name", read_only=True)
    shelf_code = serializers.CharField(source="shelf.code", read_only=True)
    full_location = serializers.CharField(source="get_full_location", read_only=True)
    available_capacity = serializers.SerializerMethodField()

    class Meta:
        model = Bin
        fields = [
            "id",
            "code",
            "name",
            "shelf",
            "shelf_name",
            "shelf_code",
            "description",
            "capacity",
            "used_capacity",
            "available_capacity",
            "length",
            "width",
            "depth",
            "full_location",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_available_capacity(self, obj: Bin) -> float:
        """Get available capacity."""
        return obj.get_available_capacity()


class WarehouseDetailSerializer(WarehouseSerializer):
    """Detailed serializer for Warehouse with nested zones."""

    zones = ZoneSerializer(many=True, read_only=True)

    class Meta(WarehouseSerializer.Meta):
        fields = WarehouseSerializer.Meta.fields + ["zones"]


class ZoneDetailSerializer(ZoneSerializer):
    """Detailed serializer for Zone with nested rows."""

    rows = RowSerializer(many=True, read_only=True)

    class Meta(ZoneSerializer.Meta):
        fields = ZoneSerializer.Meta.fields + ["rows"]


class RowDetailSerializer(RowSerializer):
    """Detailed serializer for Row with nested shelves."""

    shelves = ShelfSerializer(many=True, read_only=True)

    class Meta(RowSerializer.Meta):
        fields = RowSerializer.Meta.fields + ["shelves"]


class ShelfDetailSerializer(ShelfSerializer):
    """Detailed serializer for Shelf with nested bins."""

    bins = BinSerializer(many=True, read_only=True)

    class Meta(ShelfSerializer.Meta):
        fields = ShelfSerializer.Meta.fields + ["bins"]
