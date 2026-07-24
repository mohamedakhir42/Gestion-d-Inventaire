"""
Base service classes for business logic.
"""

from typing import Any, TypeVar

from django.db import models

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseService:
    """Base service class for business logic."""

    model: type[ModelType] = None

    def __init__(self, model: type[ModelType] = None) -> None:
        """Initialize service with model."""
        if model is not None:
            self.model = model

    def get_queryset(self) -> models.QuerySet:
        """Get base queryset for the model."""
        if self.model is None:
            raise ValueError("Model must be set for this service")
        return self.model.objects.all()

    def get_by_id(self, id: Any) -> ModelType:
        """Get instance by ID."""
        return self.get_queryset().get(id=id)

    def create(self, **kwargs) -> ModelType:
        """Create new instance."""
        return self.model.objects.create(**kwargs)

    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Update instance."""
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: ModelType) -> None:
        """Delete instance."""
        if hasattr(instance, "soft_delete"):
            instance.soft_delete()
        else:
            instance.delete()
