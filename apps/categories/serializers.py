"""
Serializers for categories app.
"""

from rest_framework import serializers

from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    parent_name = serializers.CharField(source="parent.name", read_only=True)
    full_path = serializers.CharField(source="get_full_path", read_only=True)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "code",
            "description",
            "parent",
            "parent_name",
            "image",
            "is_active",
            "full_path",
            "children_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_children_count(self, obj: Category) -> int:
        """Get count of direct children."""
        return obj.children.count()


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Serializer for category tree structure."""

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "code",
            "description",
            "image",
            "is_active",
            "children",
        ]

    def get_children(self, obj: Category) -> list:
        """Get children categories recursively."""
        children = obj.children.filter(is_deleted=False, is_active=True)
        return CategoryTreeSerializer(children, many=True).data
