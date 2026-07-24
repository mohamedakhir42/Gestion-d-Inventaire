"""
URL configuration for suppliers app.
"""

from django.urls import path

from apps.suppliers.views import SupplierDetailView, SupplierListView

app_name = "suppliers"

urlpatterns = [
    path("", SupplierListView.as_view(), name="supplier_list"),
    path("<uuid:id>/", SupplierDetailView.as_view(), name="supplier_detail"),
]
