"""
API views for categories app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer, CategoryTreeSerializer
from common.permissions import IsActiveUser


class CategoryListView(generics.ListCreateAPIView):
    """List and create categories."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = CategorySerializer
    filterset_fields = ["is_active", "parent"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        """Get category queryset."""
        return Category.objects.filter(is_deleted=False)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a category."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        """Get category queryset."""
        return Category.objects.filter(is_deleted=False)


class CategoryTreeView(generics.ListAPIView):
    """Get category tree structure."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = CategoryTreeSerializer

    def get_queryset(self):
        """Get root categories."""
        return Category.objects.filter(is_deleted=False, is_active=True, parent=None)
