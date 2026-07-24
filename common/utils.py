"""
Utility functions and helpers.
"""

import logging
import uuid
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)


def generate_unique_code(prefix: str = "", length: int = 8) -> str:
    """Generate a unique code with optional prefix."""
    unique_id = uuid.uuid4().hex[:length].upper()
    return f"{prefix}{unique_id}" if prefix else unique_id


def cache_get(key: str, default: Any = None) -> Any:
    """Get value from cache."""
    return cache.get(key, default)


def cache_set(key: str, value: Any, timeout: int = None) -> None:
    """Set value in cache."""
    if timeout is None:
        timeout = getattr(settings, "CACHE_TIMEOUT", 300)
    cache.set(key, value, timeout)


def cache_delete(key: str) -> None:
    """Delete value from cache."""
    cache.delete(key)


def cache_clear() -> None:
    """Clear all cache."""
    cache.clear()


def get_client_ip(request: Any) -> str:
    """Get client IP address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


def format_datetime(dt: Any) -> str:
    """Format datetime for display."""
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S") if hasattr(dt, "strftime") else str(dt)


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    import re

    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    return filename


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def get_upload_path(instance: Any, filename: str) -> str:
    """Generate upload path for file storage."""
    from django.utils.text import slugify

    model_name = instance.__class__.__name__.lower()
    sanitized_filename = sanitize_filename(filename)
    return f"{model_name}/{timezone.now().strftime('%Y/%m')}/{sanitized_filename}"
