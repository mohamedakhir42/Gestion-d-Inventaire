"""
Data selectors for stock app.
"""

from django.db.models import Q

from common.selectors import BaseSelector

from apps.stock.models import Stock, StockReservation


class StockSelector(BaseSelector):
    """Selector for Stock model."""

    model = Stock

    def get_by_product_and_warehouse(self, product_id, warehouse_id):
        """Get stock by product and warehouse."""
        return self.get_queryset().get(product_id=product_id, warehouse_id=warehouse_id)

    def get_by_product(self, product_id):
        """Get all stock records for a product."""
        return self.filter(product_id=product_id)

    def get_by_warehouse(self, warehouse_id):
        """Get all stock records in a warehouse."""
        return self.filter(warehouse_id=warehouse_id)

    def get_low_stock(self):
        """Get stocks below minimum level."""
        return self.filter(quantity__lt=models.F("minimum_level"))

    def get_reorder_stock(self):
        """Get stocks below reorder level."""
        return self.filter(quantity__lt=models.F("reorder_level"))

    def get_overstock(self):
        """Get stocks above maximum level."""
        return self.filter(quantity__gt=models.F("maximum_level"))

    def search_stock(self, query):
        """Search stock by product name or code."""
        return self.filter(
            Q(product__name__icontains=query) | Q(product__internal_code__icontains=query)
        )


class StockReservationSelector(BaseSelector):
    """Selector for StockReservation model."""

    model = StockReservation

    def get_by_stock(self, stock_id):
        """Get reservations for a stock."""
        return self.filter(stock_id=stock_id)

    def get_by_status(self, status):
        """Get reservations by status."""
        return self.filter(status=status)

    def get_active_reservations(self):
        """Get active (pending or confirmed) reservations."""
        return self.filter(status__in=[StockReservation.Status.PENDING, StockReservation.Status.CONFIRMED])

    def get_expired_reservations(self):
        """Get expired pending reservations."""
        from django.utils import timezone

        return self.filter(
            status=StockReservation.Status.PENDING,
            reserved_until__lt=timezone.now(),
        )
