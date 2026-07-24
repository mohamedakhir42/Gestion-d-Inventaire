"""
Business logic services for stock app.
"""

from django.utils.translation import gettext_lazy as _

from apps.stock.models import Stock, StockReservation
from common.services import BaseService
from common.utils import generate_unique_code


class StockService(BaseService):
    """Service for stock management."""

    model = Stock

    def create_stock(self, data: dict) -> Stock:
        """Create a new stock record."""
        stock = self.create(**data)
        stock.calculate_available_quantity()
        return stock

    def update_stock_quantity(self, stock: Stock, quantity: float, movement_type: str) -> None:
        """Update stock quantity based on movement type."""
        if movement_type in ["ENTRY", "RETURN"]:
            stock.quantity += quantity
        elif movement_type in ["EXIT", "CONSUMPTION", "DAMAGE", "LOSS"]:
            stock.quantity -= quantity
        elif movement_type == "ADJUSTMENT":
            stock.quantity = quantity
        elif movement_type == "TRANSFER_IN":
            stock.quantity += quantity
        elif movement_type == "TRANSFER_OUT":
            stock.quantity -= quantity

        stock.calculate_available_quantity()
        stock.save()

    def perform_stock_count(self, stock: Stock, counted_quantity: float) -> None:
        """Perform stock count and calculate variance."""
        stock.calculate_variance(counted_quantity)
        if stock.quantity != counted_quantity:
            # Create adjustment movement for variance
            from apps.movements.models import Movement
            from apps.movements.services import MovementService

            movement_service = MovementService()
            movement_service.create_movement(
                {
                    "movement_type": Movement.Type.ADJUSTMENT,
                    "product": stock.product,
                    "warehouse": stock.warehouse,
                    "quantity": counted_quantity,
                    "reason": f"Stock count adjustment. Variance: {stock.variance}",
                    "reference_number": generate_unique_code("SC-", 10),
                    "performed_by": None,  # System user
                }
            )


class StockReservationService(BaseService):
    """Service for stock reservation management."""

    model = StockReservation

    def create_reservation(self, data: dict, user) -> StockReservation:
        """Create a new stock reservation."""
        if "reference_number" not in data:
            data["reference_number"] = generate_unique_code("RES-", 10)
        data["reserved_by"] = user
        return self.create(**data)

    def confirm_reservation(self, reservation: StockReservation) -> None:
        """Confirm a reservation."""
        reservation.confirm_reservation()

    def cancel_reservation(self, reservation: StockReservation) -> None:
        """Cancel a reservation."""
        reservation.cancel_reservation()

    def fulfill_reservation(self, reservation: StockReservation) -> None:
        """Fulfill a reservation."""
        reservation.fulfill_reservation()

    def expire_reservations(self) -> int:
        """Expire pending reservations past their reserved_until time."""
        from django.utils import timezone

        expired = StockReservation.objects.filter(
            status=StockReservation.Status.PENDING,
            reserved_until__lt=timezone.now(),
        )
        count = expired.count()
        expired.update(status=StockReservation.Status.CANCELLED)
        return count
