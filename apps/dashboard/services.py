"""
Analytics and reporting services for dashboard.
"""

from datetime import datetime, timedelta
from typing import Any, Dict

from django.db.models import Count, Q, Sum, Avg, F
from django.db.models.functions import Coalesce

from apps.inventory.models import Product
from apps.movements.models import Movement, StockRequest
from apps.stock.models import Stock
from apps.warehouses.models import Warehouse


class DashboardService:
    """Service for dashboard analytics and reporting."""

    def get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics for dashboard."""
        return {
            "total_products": Product.objects.filter(is_deleted=False).count(),
            "total_warehouses": Warehouse.objects.filter(is_deleted=False).count(),
            "total_stock_value": self.calculate_total_stock_value(),
            "low_stock_items": self.get_low_stock_count(),
            "pending_requests": StockRequest.objects.filter(status=StockRequest.Status.PENDING, is_deleted=False).count(),
            "today_movements": Movement.objects.filter(
                movement_date__date=datetime.now().date(),
                is_deleted=False,
            ).count(),
        }

    def calculate_total_stock_value(self) -> float:
        """Calculate total stock value across all warehouses."""
        result = Stock.objects.aggregate(
            total_value=Sum(F("quantity") * F("product__average_cost"))
        )
        return result["total_value"] or 0

    def get_low_stock_count(self) -> int:
        """Get count of items below minimum stock level."""
        return Stock.objects.filter(quantity__lt=F("minimum_level"), is_deleted=False).count()

    def get_stock_by_warehouse(self) -> list:
        """Get stock distribution by warehouse."""
        warehouses = Warehouse.objects.filter(is_deleted=False).annotate(
            total_quantity=Coalesce(Sum("stocks__quantity"), 0),
            total_value=Coalesce(Sum(F("stocks__quantity") * F("stocks__product__average_cost")), 0),
        ).values("code", "name", "total_quantity", "total_value")
        return list(warehouses)

    def get_movement_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get movement statistics for specified period."""
        since = datetime.now() - timedelta(days=days)
        movements = Movement.objects.filter(movement_date__gte=since, is_deleted=False)

        return {
            "total_movements": movements.count(),
            "by_type": movements.values("movement_type").annotate(
                count=Count("id"),
                total_quantity=Sum("quantity"),
            ),
            "by_status": movements.values("status").annotate(count=Count("id")),
        }

    def get_top_products(self, limit: int = 10) -> list:
        """Get top products by movement quantity."""
        since = datetime.now() - timedelta(days=30)
        top_products = (
            Movement.objects.filter(movement_date__gte=since, is_deleted=False)
            .values("product__internal_code", "product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:limit]
        )
        return list(top_products)

    def get_request_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get stock request statistics."""
        since = datetime.now() - timedelta(days=days)
        requests = StockRequest.objects.filter(requested_at__gte=since, is_deleted=False)

        return {
            "total_requests": requests.count(),
            "by_status": requests.values("status").annotate(count=Count("id")),
            "by_priority": requests.values("priority").annotate(count=Count("id")),
            "avg_completion_time": self.calculate_avg_completion_time(requests),
        }

    def calculate_avg_completion_time(self, requests) -> float:
        """Calculate average completion time for requests."""
        completed = requests.filter(status=StockRequest.Status.COMPLETED)
        if not completed.exists():
            return 0

        total_time = sum(
            (r.completed_at - r.requested_at).total_seconds() for r in completed if r.completed_at
        )
        return total_time / completed.count() / 3600  # Convert to hours

    def get_warehouse_utilization(self) -> list:
        """Get warehouse utilization statistics."""
        warehouses = Warehouse.objects.filter(is_deleted=False)
        utilization_data = []

        for warehouse in warehouses:
            total_capacity = warehouse.get_total_capacity()
            used_capacity = warehouse.get_used_capacity()
            utilization_percentage = (used_capacity / total_capacity * 100) if total_capacity > 0 else 0

            utilization_data.append(
                {
                    "warehouse_code": warehouse.code,
                    "warehouse_name": warehouse.name,
                    "total_capacity": total_capacity,
                    "used_capacity": used_capacity,
                    "utilization_percentage": round(utilization_percentage, 2),
                }
            )

        return utilization_data

    def get_category_distribution(self) -> list:
        """Get product distribution by category."""
        from apps.categories.models import Category

        categories = Category.objects.filter(is_deleted=False).annotate(
            product_count=Count("products"),
            total_stock=Sum("products__stock__quantity"),
        ).values("name", "code", "product_count", "total_stock")

        return list(categories)

    def get_recent_activity(self, limit: int = 20) -> list:
        """Get recent activity across the system."""
        from apps.audit.models import AuditLog

        recent_logs = AuditLog.objects.order_by("-timestamp")[:limit]
        return [
            {
                "action": log.action,
                "entity_type": log.entity_type,
                "user_email": log.user_email,
                "timestamp": log.timestamp,
                "description": log.description,
            }
            for log in recent_logs
        ]


class ReportService:
    """Service for generating reports."""

    def generate_inventory_report(self, warehouse_id=None) -> Dict[str, Any]:
        """Generate inventory report."""
        stocks = Stock.objects.filter(is_deleted=False)
        if warehouse_id:
            stocks = stocks.filter(warehouse_id=warehouse_id)

        return {
            "report_type": "inventory",
            "generated_at": datetime.now(),
            "total_items": stocks.count(),
            "total_value": stocks.aggregate(total=Sum(F("quantity") * F("product__average_cost")))["total"] or 0,
            "low_stock_items": stocks.filter(quantity__lt=F("minimum_level")).count(),
            "overstock_items": stocks.filter(quantity__gt=F("maximum_level")).count(),
            "items": list(
                stocks.values(
                    "product__internal_code",
                    "product__name",
                    "warehouse__code",
                    "quantity",
                    "available_quantity",
                    "minimum_level",
                    "maximum_level",
                )
            ),
        }

    def generate_movement_report(self, start_date, end_date, warehouse_id=None) -> Dict[str, Any]:
        """Generate movement report for date range."""
        movements = Movement.objects.filter(
            movement_date__date__range=[start_date, end_date],
            is_deleted=False,
        )
        if warehouse_id:
            movements = movements.filter(warehouse_id=warehouse_id)

        return {
            "report_type": "movement",
            "generated_at": datetime.now(),
            "period": {"start": start_date, "end": end_date},
            "total_movements": movements.count(),
            "by_type": list(movements.values("movement_type").annotate(count=Count("id"), total_quantity=Sum("quantity"))),
            "movements": list(
                movements.values(
                    "reference_number",
                    "movement_type",
                    "product__internal_code",
                    "warehouse__code",
                    "quantity",
                    "movement_date",
                )
            ),
        }

    def generate_request_report(self, start_date, end_date) -> Dict[str, Any]:
        """Generate stock request report."""
        requests = StockRequest.objects.filter(
            requested_at__date__range=[start_date, end_date],
            is_deleted=False,
        )

        return {
            "report_type": "stock_request",
            "generated_at": datetime.now(),
            "period": {"start": start_date, "end": end_date},
            "total_requests": requests.count(),
            "by_status": list(requests.values("status").annotate(count=Count("id"))),
            "by_priority": list(requests.values("priority").annotate(count=Count("id"))),
            "requests": list(
                requests.values(
                    "reference_number",
                    "title",
                    "status",
                    "priority",
                    "warehouse__code",
                    "requested_by__email",
                    "requested_at",
                )
            ),
        }
