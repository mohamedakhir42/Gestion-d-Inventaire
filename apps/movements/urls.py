"""
URL configuration for movements app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.movements.views import MovementViewSet, StockRequestViewSet

app_name = "movements"

router = DefaultRouter()
router.register(r"movements", MovementViewSet, basename="movement")
router.register(r"requests", StockRequestViewSet, basename="stockrequest")

urlpatterns = [
    path("", include(router.urls)),
]
