"""
URL configuration for warehouses app.
"""

from django.urls import path

from apps.warehouses.views import (
    BinDetailView,
    BinListView,
    RowDetailView,
    RowListView,
    ShelfDetailView,
    ShelfListView,
    WarehouseDetailView,
    WarehouseListView,
    ZoneDetailView,
    ZoneListView,
)

app_name = "warehouses"

urlpatterns = [
    # Warehouses
    path("", WarehouseListView.as_view(), name="warehouse_list"),
    path("<uuid:id>/", WarehouseDetailView.as_view(), name="warehouse_detail"),
    # Zones
    path("<uuid:warehouse_id>/zones/", ZoneListView.as_view(), name="zone_list"),
    path("zones/<uuid:id>/", ZoneDetailView.as_view(), name="zone_detail"),
    # Rows
    path("zones/<uuid:zone_id>/rows/", RowListView.as_view(), name="row_list"),
    path("rows/<uuid:id>/", RowDetailView.as_view(), name="row_detail"),
    # Shelves
    path("rows/<uuid:row_id>/shelves/", ShelfListView.as_view(), name="shelf_list"),
    path("shelves/<uuid:id>/", ShelfDetailView.as_view(), name="shelf_detail"),
    # Bins
    path("shelves/<uuid:shelf_id>/bins/", BinListView.as_view(), name="bin_list"),
    path("bins/<uuid:id>/", BinDetailView.as_view(), name="bin_detail"),
]
