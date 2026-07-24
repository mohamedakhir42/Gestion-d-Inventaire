"""
Business logic services for inventory app.
"""

import qrcode
from io import BytesIO

from django.core.files import File
from django.utils.translation import gettext_lazy as _

from apps.inventory.models import Brand, Product, Unit
from common.services import BaseService
from common.utils import generate_unique_code


class BrandService(BaseService):
    """Service for brand management."""

    model = Brand

    def create_brand(self, data: dict) -> Brand:
        """Create a new brand."""
        if "code" not in data:
            data["code"] = generate_unique_code("BRD-", 6)
        return self.create(**data)


class UnitService(BaseService):
    """Service for unit management."""

    model = Unit

    def create_unit(self, data: dict) -> Unit:
        """Create a new unit."""
        if "code" not in data:
            data["code"] = generate_unique_code("UNT-", 4)
        return self.create(**data)


class ProductService(BaseService):
    """Service for product management."""

    model = Product

    def create_product(self, data: dict, user) -> Product:
        """Create a new product with QR code generation."""
        if "qr_code" not in data or not data["qr_code"]:
            data["qr_code"] = generate_unique_code("QR-", 12)

        product = self.create(
            **data,
            created_by=user,
            updated_by=user,
        )

        # Generate QR code image
        self.generate_qr_code(product)

        return product

    def generate_qr_code(self, product: Product) -> None:
        """Generate QR code for product."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(product.qr_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Save QR code as product image if not set
        if not product.image:
            product.image.save(f"qr_{product.qr_code}.png", File(buffer), save=False)
            product.save()

    def update_stock(self, product: Product, quantity: float, movement_type: str) -> None:
        """Update product stock based on movement type."""
        if movement_type in ["ENTRY", "RETURN"]:
            product.current_stock += quantity
        elif movement_type in ["EXIT", "CONSUMPTION", "DAMAGE", "LOSS"]:
            product.current_stock -= quantity
        elif movement_type == "ADJUSTMENT":
            product.current_stock = quantity

        product.calculate_available_stock()
        product.save()

    def calculate_average_cost(self, product: Product, new_quantity: float, new_cost: float) -> None:
        """Calculate weighted average cost."""
        if product.current_stock > 0:
            total_value = (product.current_stock * product.average_cost) + (new_quantity * new_cost)
            total_quantity = product.current_stock + new_quantity
            product.average_cost = total_value / total_quantity
        else:
            product.average_cost = new_cost
        product.save()
