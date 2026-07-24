"""
URL configuration for Inventory Management System.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/inventory/", include("apps.inventory.urls")),
    path("api/warehouses/", include("apps.warehouses.urls")),
    path("api/stock/", include("apps.stock.urls")),
    path("api/movements/", include("apps.movements.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/audit/", include("apps.audit.urls")),
    path("api/categories/", include("apps.categories.urls")),
    path("api/suppliers/", include("apps.suppliers.urls")),
    path("api/locations/", include("apps.locations.urls")),
    path("health/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
