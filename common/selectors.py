"""
Base selector classes for data retrieval.
"""

from typing import Any, TypeVar

from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseSelector:
    """Base selector class for data retrieval."""

    model: type[ModelType] = None

    def __init__(self, model: type[ModelType] = None) -> None:
        """Initialize selector with model."""
        if model is not None:
            self.model = model

    def get_queryset(self) -> models.QuerySet:
        """Get base queryset."""
        if self.model is None:
            raise ValueError("Model must be set for this selector")
        return self.model.objects.all()

    def get_by_id(self, id: Any) -> ModelType:
        """Get instance by ID."""
        return self.get_queryset().get(id=id)

    def get_all(self) -> models.QuerySet:
        """Get all instances."""
        return self.get_queryset()

    def filter(self, **kwargs) -> models.QuerySet:
        """Filter instances."""
        return self.get_queryset().filter(**kwargs)

    def exists(self, **kwargs) -> bool:
        """Check if instance exists."""
        return self.get_queryset().filter(**kwargs).exists()

    def count(self, **kwargs) -> int:
        """Count instances."""
        return self.get_queryset().filter(**kwargs).count()
