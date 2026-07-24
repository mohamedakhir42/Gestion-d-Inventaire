"""
Admin configuration for core models.
"""

from django.contrib import admin


class SoftDeleteAdmin(admin.ModelAdmin):
    """Admin interface for soft delete models."""

    def get_queryset(self, request):
        """Return queryset including soft-deleted objects."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)

    def delete_model(self, request, obj):
        """Override delete to use soft delete."""
        if hasattr(obj, "soft_delete"):
            obj.soft_delete(user=request.user)
        else:
            super().delete_model(request, obj)
