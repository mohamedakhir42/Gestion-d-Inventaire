"""
Data selectors for movements app.
"""

from django.db.models import Q

from common.selectors import BaseSelector

from apps.movements.models import Movement, StockRequest


class MovementSelector(BaseSelector):
    """Selector for Movement model."""

    model = Movement

    def get_by_reference(self, reference: str):
        """Get movement by reference number."""
        return self.get_queryset().get(reference_number=reference)

    def get_by_type(self, movement_type: str):
        """Get movements by type."""
        return self.filter(movement_type=movement_type)

    def get_by_status(self, status: str):
        """Get movements by status."""
        return self.filter(status=status)

    def get_by_product(self, product_id):
        """Get movements for a product."""
        return self.filter(product_id=product_id)

    def get_by_warehouse(self, warehouse_id):
        """Get movements for a warehouse."""
        return self.filter(warehouse_id=warehouse_id)

    def get_by_user(self, user):
        """Get movements by user."""
        return self.filter(requested_by=user)

    def get_pending_movements(self):
        """Get pending movements."""
        return self.filter(status=Movement.Status.PENDING)

    def search_movements(self, query: str):
        """Search movements by reference or product."""
        return self.filter(
            Q(reference_number__icontains=query) | Q(product__name__icontains=query) | Q(product__internal_code__icontains=query)
        )


class StockRequestSelector(BaseSelector):
    """Selector for StockRequest model."""

    model = StockRequest

    def get_by_reference(self, reference: str):
        """Get request by reference number."""
        return self.get_queryset().get(reference_number=reference)

    def get_by_status(self, status: str):
        """Get requests by status."""
        return self.filter(status=status)

    def get_by_priority(self, priority: str):
        """Get requests by priority."""
        return self.filter(priority=priority)

    def get_by_warehouse(self, warehouse_id):
        """Get requests by warehouse."""
        return self.filter(warehouse_id=warehouse_id)

    def get_by_user(self, user):
        """Get requests by user."""
        return self.filter(requested_by=user)

    def get_pending_requests(self):
        """Get pending requests."""
        return self.filter(status=StockRequest.Status.PENDING)

    def get_urgent_requests(self):
        """Get urgent requests."""
        return self.filter(priority=StockRequest.Priority.URGENT, status=StockRequest.Status.PENDING)

    def search_requests(self, query: str):
        """Search requests by title or reference."""
        return self.filter(Q(title__icontains=query) | Q(reference_number__icontains=query))
