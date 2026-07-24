"""
Business logic services for movements app.
"""

from django.utils.translation import gettext_lazy as _

from apps.movements.models import Movement, StockRequest, StockRequestItem
from apps.stock.models import Stock
from apps.stock.services import StockService
from common.services import BaseService
from common.utils import generate_unique_code


class MovementService(BaseService):
    """Service for movement management."""

    model = Movement

    def create_movement(self, data: dict) -> Movement:
        """Create a new movement."""
        if "reference_number" not in data:
            data["reference_number"] = generate_unique_code("MOV-", 10)

        # Calculate total cost if unit cost provided
        if data.get("unit_cost") and data.get("quantity"):
            data["total_cost"] = float(data["unit_cost"]) * float(data["quantity"])

        movement = self.create(**data)
        return movement

    def approve_movement(self, movement: Movement, user) -> None:
        """Approve a movement."""
        movement.approve(user)

    def validate_movement(self, movement: Movement, user) -> None:
        """Validate a movement."""
        movement.validate(user)

    def complete_movement(self, movement: Movement, user) -> None:
        """Complete a movement and update stock."""
        movement.complete(user)

    def cancel_movement(self, movement: Movement, user) -> None:
        """Cancel a movement."""
        movement.cancel(user)

    def create_movement_from_request(self, stock_request: StockRequest, user) -> Movement:
        """Create movements from a stock request."""
        movements = []
        for item in stock_request.items:
            movement = self.create_movement(
                {
                    "movement_type": Movement.Type.EXIT,
                    "product": item.product,
                    "warehouse": stock_request.warehouse,
                    "quantity": item.quantity,
                    "reason": f"Stock request: {stock_request.reference_number}",
                    "reference_number": generate_unique_code("MOV-", 10),
                    "requested_by": user,
                }
            )
            movements.append(movement)
        return movements


class StockRequestService(BaseService):
    """Service for stock request management."""

    model = StockRequest

    def create_request(self, data: dict, user) -> StockRequest:
        """Create a new stock request."""
        if "reference_number" not in data:
            data["reference_number"] = generate_unique_code("REQ-", 10)
        data["requested_by"] = user
        return self.create(**data)

    def approve_request(self, stock_request: StockRequest, user) -> None:
        """Approve a stock request."""
        stock_request.approve(user)

    def reject_request(self, stock_request: StockRequest, user, reason: str) -> None:
        """Reject a stock request."""
        stock_request.reject(user, reason)

    def validate_request(self, stock_request: StockRequest, user) -> None:
        """Validate a stock request."""
        stock_request.validate(user)

    def complete_request(self, stock_request: StockRequest) -> None:
        """Complete a stock request."""
        stock_request.complete()

    def cancel_request(self, stock_request: StockRequest) -> None:
        """Cancel a stock request."""
        stock_request.cancel()

    def get_pending_requests(self):
        """Get pending stock requests."""
        return self.filter(status=StockRequest.Status.PENDING)

    def get_requests_by_user(self, user):
        """Get requests by user."""
        return self.filter(requested_by=user)

    def get_requests_by_warehouse(self, warehouse_id):
        """Get requests by warehouse."""
        return self.filter(warehouse_id=warehouse_id)
