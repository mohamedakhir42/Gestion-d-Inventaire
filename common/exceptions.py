"""
Custom exceptions for the application.
"""

from typing import Any, Optional

from rest_framework.exceptions import APIException, ValidationError as DRFValidationError


class BaseAPIException(APIException):
    """Base exception for custom API errors."""

    status_code: int = 400
    default_detail: str = "A server error occurred."
    default_code: str = "error"

    def __init__(self, detail: Any = None, code: Optional[str] = None) -> None:
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        self.detail = {"detail": detail, "code": code}
        super().__init__(detail=detail, code=code)


class ValidationError(BaseAPIException):
    """Validation error exception."""

    status_code = 400
    default_detail = "Invalid input."
    default_code = "validation_error"


class AuthenticationError(BaseAPIException):
    """Authentication error exception."""

    status_code = 401
    default_detail = "Authentication failed."
    default_code = "authentication_error"


class PermissionDenied(BaseAPIException):
    """Permission denied exception."""

    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class NotFoundError(BaseAPIException):
    """Not found error exception."""

    status_code = 404
    default_detail = "Resource not found."
    default_code = "not_found"


class ConflictError(BaseAPIException):
    """Conflict error exception."""

    status_code = 409
    default_detail = "Resource conflict."
    default_code = "conflict"


class RateLimitError(BaseAPIException):
    """Rate limit error exception."""

    status_code = 429
    default_detail = "Rate limit exceeded."
    default_code = "rate_limit_exceeded"


class ServiceUnavailableError(BaseAPIException):
    """Service unavailable error exception."""

    status_code = 503
    default_detail = "Service temporarily unavailable."
    default_code = "service_unavailable"


def custom_exception_handler(exc: Exception, context: dict) -> dict:
    """Custom exception handler for DRF."""
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {"detail": response.data.get("detail", str(response.data))}

        if isinstance(exc, BaseAPIException):
            custom_response_data["code"] = exc.detail.get("code", "error")

        response.data = custom_response_data

    return response
