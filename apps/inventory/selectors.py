"""
Data selectors for inventory app.
"""

from django.db.models import Q

from common.selectors import BaseSelector

from apps.inventory.models import Brand, Product, Unit


class ProductSelector(BaseSelector):
    """Selector for Product model."""

    model = Product

    def get_by_internal_code(self, code: str):
        """Get product by internal code."""
        return self.get_queryset().get(internal_code=code)

    def get_by_barcode(self, barcode: str):
        """Get product by barcode."""
        return self.get_queryset().get(barcode=barcode)

    def get_by_qr_code(self, qr_code: str):
        """Get product by QR code."""
        return self.get_queryset().get(qr_code=qr_code)

    def search_products(self, query: str):
        """Search products by various fields."""
        return self.filter(
            Q(name__icontains=query)
            | Q(internal_code__icontains=query)
            | Q(barcode__icontains=query)
            | Q(description__icontains=query)
        )

    def get_by_category(self, category_id):
        """Get products by category."""
        return self.filter(category_id=category_id)

    def get_by_brand(self, brand_id):
        """Get products by brand."""
        return self.filter(brand_id=brand_id)

    def get_by_supplier(self, supplier_id):
        """Get products by supplier."""
        return self.filter(supplier_id=supplier_id)

    def get_low_stock_products(self):
        """Get products below minimum stock."""
        return self.filter(current_stock__lt=models.F("minimum_stock"))

    def get_overstock_products(self):
        """Get products above maximum stock."""
        return self.filter(current_stock__gt=models.F("maximum_stock"))


class BrandSelector(BaseSelector):
    """Selector for Brand model."""

    model = Brand

    def get_active_brands(self):
        """Get active brands."""
        return self.filter(is_active=True)


class UnitSelector(BaseSelector):
    """Selector for Unit model."""

    model = Unit

    def get_active_units(self):
        """Get active units."""
        return self.filter(is_active=True)

    def get_base_units(self):
        """Get base units."""
        return self.filter(is_base_unit=True)
