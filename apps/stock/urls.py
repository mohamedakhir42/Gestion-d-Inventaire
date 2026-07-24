"""
URL configuration for stock app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.stock.views import StockReservationViewSet, StockViewSet

app_name = "stock"

router = DefaultRouter()
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"reservations", StockReservationViewSet, basename="stockreservation")

urlpatterns = [
    path("", include(router.urls)),
]
