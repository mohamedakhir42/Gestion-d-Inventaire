"""
URL configuration for locations app.
"""

from django.urls import path

from apps.locations.views import ProductLocationDetailView, ProductLocationListView

app_name = "locations"

urlpatterns = [
    path("", ProductLocationListView.as_view(), name="product_location_list"),
    path("<uuid:id>/", ProductLocationDetailView.as_view(), name="product_location_detail"),
]
