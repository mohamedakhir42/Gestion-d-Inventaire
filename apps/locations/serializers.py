"""
Serializers for locations app.
"""

from rest_framework import serializers

from apps.locations.models import ProductLocation


class ProductLocationSerializer(serializers.ModelSerializer):
    """Serializer for ProductLocation model."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.internal_code", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    warehouse_code = serializers.CharField(source="warehouse.code", read_only=True)
    bin_code = serializers.CharField(source="bin.code", read_only=True)
    full_location = serializers.CharField(source="get_full_location", read_only=True)

    class Meta:
        model = ProductLocation
        fields = [
            "id",
            "product",
            "product_name",
            "product_code",
            "warehouse",
            "warehouse_name",
            "warehouse_code",
            "zone",
            "row",
            "shelf",
            "bin",
            "bin_code",
            "quantity",
            "is_primary",
            "full_location",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
