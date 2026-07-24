"""
Core URL configuration.
"""

from django.http import JsonResponse
from django.urls import path


def health_check(request):
    """Health check endpoint."""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "inventory-management-system",
        }
    )


urlpatterns = [
    path("", health_check, name="health-check"),
]
