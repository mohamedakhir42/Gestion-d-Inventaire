"""
URL configuration for dashboard app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.dashboard.views import DashboardViewSet, ReportViewSet

app_name = "dashboard"

router = DefaultRouter()
router.register(r"", DashboardViewSet, basename="dashboard")
router.register(r"reports", ReportViewSet, basename="report")

urlpatterns = [
    path("", include(router.urls)),
]
