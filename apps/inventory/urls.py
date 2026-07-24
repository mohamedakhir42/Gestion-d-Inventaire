"""
URL configuration for inventory app.
"""

from django.urls import path

from apps.inventory.views import (
    BrandDetailView,
    BrandListView,
    ProductByBarcodeView,
    ProductDetailView,
    ProductListView,
    UnitDetailView,
    UnitListView,
)

app_name = "inventory"

urlpatterns = [
    # Brands
    path("brands/", BrandListView.as_view(), name="brand_list"),
    path("brands/<uuid:id>/", BrandDetailView.as_view(), name="brand_detail"),
    # Units
    path("units/", UnitListView.as_view(), name="unit_list"),
    path("units/<uuid:id>/", UnitDetailView.as_view(), name="unit_detail"),
    # Products
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<uuid:id>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/barcode/<str:barcode>/", ProductByBarcodeView.as_view(), name="product_by_barcode"),
]
