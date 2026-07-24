"""
Custom middleware for the application.
"""

import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all incoming requests."""

    def process_request(self, request: HttpRequest) -> None:
        """Log incoming request details."""
        logger.info(
            f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}",
        )

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Log response details."""
        logger.info(
            f"Response: {response.status_code} for {request.method} {request.path}",
        )
        return response


class AuditMiddleware(MiddlewareMixin):
    """Middleware to capture request context for audit logging."""

    def process_request(self, request: HttpRequest) -> None:
        """Store request context for audit."""
        request.audit_context = {
            "ip_address": self.get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
            "path": request.path,
            "method": request.method,
        }

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """Get client IP address from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
