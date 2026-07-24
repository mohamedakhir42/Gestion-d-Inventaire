"""
Custom validators for the application.
"""

import re
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PasswordComplexityValidator:
    """Validator for password complexity."""

    def __init__(
        self,
        min_uppercase: int = 1,
        min_lowercase: int = 1,
        min_digits: int = 1,
        min_special: int = 1,
    ) -> None:
        self.min_uppercase = min_uppercase
        self.min_lowercase = min_lowercase
        self.min_digits = min_digits
        self.min_special = min_special

    def validate(self, password: str, user: Any = None) -> None:
        """Validate password complexity."""
        if len([c for c in password if c.isupper()]) < self.min_uppercase:
            raise ValidationError(
                _(f"Password must contain at least {self.min_uppercase} uppercase letter(s)."),
                code="password_no_uppercase",
            )

        if len([c for c in password if c.islower()]) < self.min_lowercase:
            raise ValidationError(
                _(f"Password must contain at least {self.min_lowercase} lowercase letter(s)."),
                code="password_no_lowercase",
            )

        if len([c for c in password if c.isdigit()]) < self.min_digits:
            raise ValidationError(
                _(f"Password must contain at least {self.min_digits} digit(s)."),
                code="password_no_digit",
            )

        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if len([c for c in password if c in special_chars]) < self.min_special:
            raise ValidationError(
                _(f"Password must contain at least {self.min_special} special character(s)."),
                code="password_no_special",
            )

    def get_help_text(self) -> str:
        """Return help text for password complexity."""
        return _(
            f"Password must contain at least {self.min_uppercase} uppercase, "
            f"{self.min_lowercase} lowercase, {self.min_digits} digit(s), "
            f"and {self.min_special} special character(s)."
        )


class PhoneValidator(RegexValidator):
    """Validator for phone numbers."""

    def __init__(self) -> None:
        super().__init__(
            regex=r"^\+?[\d\s-()]{10,20}$",
            message=_("Enter a valid phone number."),
        )


class EmployeeIDValidator(RegexValidator):
    """Validator for employee IDs."""

    def __init__(self) -> None:
        super().__init__(
            regex=r"^[A-Z0-9-]{3,20}$",
            message=_("Employee ID must be 3-20 alphanumeric characters and dashes."),
        )


class BarcodeValidator(RegexValidator):
    """Validator for barcodes."""

    def __init__(self) -> None:
        super().__init__(
            regex=r"^[A-Z0-9]{8,20}$",
            message=_("Barcode must be 8-20 alphanumeric characters."),
        )


class InternalCodeValidator(RegexValidator):
    """Validator for internal product codes."""

    def __init__(self) -> None:
        super().__init__(
            regex=r"^[A-Z0-9-]{3,30}$",
            message=_("Internal code must be 3-30 alphanumeric characters and dashes."),
        )
