"""
Serializers for inventory app.
"""

from rest_framework import serializers

from apps.categories.models import Category
from apps.inventory.models import Brand, Product, Unit
from apps.suppliers.models import Supplier


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "code",
            "description",
            "website",
            "logo",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model."""

    base_unit_name = serializers.CharField(source="base_unit.name", read_only=True)

    class Meta:
        model = Unit
        fields = [
            "id",
            "name",
            "code",
            "symbol",
            "description",
            "is_base_unit",
            "conversion_factor",
            "base_unit",
            "base_unit_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    unit_symbol = serializers.CharField(source="unit.symbol", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    is_below_minimum = serializers.BooleanField(source="is_below_minimum", read_only=True)
    is_above_maximum = serializers.BooleanField(source="is_above_maximum", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "internal_code",
            "barcode",
            "qr_code",
            "name",
            "description",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "unit",
            "unit_symbol",
            "supplier",
            "supplier_name",
            "purchase_price",
            "average_cost",
            "selling_price",
            "minimum_stock",
            "maximum_stock",
            "current_stock",
            "reserved_stock",
            "available_stock",
            "image",
            "specifications",
            "status",
            "status_display",
            "is_below_minimum",
            "is_above_maximum",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "current_stock",
            "reserved_stock",
            "available_stock",
            "created_at",
            "updated_at",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating products."""

    class Meta:
        model = Product
        fields = [
            "internal_code",
            "barcode",
            "qr_code",
            "name",
            "description",
            "category",
            "brand",
            "unit",
            "supplier",
            "purchase_price",
            "selling_price",
            "minimum_stock",
            "maximum_stock",
            "image",
            "specifications",
            "status",
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating products."""

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "brand",
            "unit",
            "supplier",
            "purchase_price",
            "selling_price",
            "minimum_stock",
            "maximum_stock",
            "image",
            "specifications",
            "status",
        ]
