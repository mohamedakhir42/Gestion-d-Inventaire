"""
Mixin classes for views and serializers.
"""

from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AuditMixin:
    """Mixin to add audit logging to views."""

    def perform_create(self, serializer: Any) -> None:
        """Perform create with audit logging."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer: Any) -> None:
        """Perform update with audit logging."""
        serializer.save(updated_by=self.request.user)


class BulkCreateModelMixin:
    """Mixin for bulk create operations."""

    def get_bulk_serializer(self, *args, **kwargs) -> Any:
        """Get serializer for bulk operations."""
        return self.get_serializer(*args, **kwargs)

    def bulk_create(self, request: Any, *args, **kwargs) -> Response:
        """Handle bulk create requests."""
        serializer = self.get_bulk_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_bulk_create(self, serializer: Any) -> None:
        """Perform bulk create."""
        serializer.save()


class BulkUpdateModelMixin:
    """Mixin for bulk update operations."""

    def bulk_update(self, request: Any, *args, **kwargs) -> Response:
        """Handle bulk update requests."""
        partial = kwargs.pop("partial", False)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, data=request.data, many=True, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_update(serializer)
        return Response(serializer.data)

    def perform_bulk_update(self, serializer: Any) -> None:
        """Perform bulk update."""
        serializer.save()


class ExportMixin:
    """Mixin for data export operations."""

    def export_to_csv(self, queryset: Any) -> Response:
        """Export data to CSV format."""
        import csv
        from io import StringIO

        from django.http import HttpResponse

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        if queryset.exists():
            writer.writerow([field.name for field in queryset.model._meta.fields])
            for obj in queryset:
                writer.writerow([getattr(obj, field.name) for field in queryset.model._meta.fields])

        return response
