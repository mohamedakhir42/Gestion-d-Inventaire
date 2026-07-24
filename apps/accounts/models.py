"""
User and authentication models.
"""

import uuid
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from common.validators import EmployeeIDValidator, PhoneValidator


class UserManager(BaseUserManager["User"]):
    """Custom user manager."""

    def create_user(
        self,
        email: str,
        password: str = None,
        **extra_fields: Any,
    ) -> "User":
        """Create and save a regular user."""
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str = None,
        **extra_fields: Any,
    ) -> "User":
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "SUPER_ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model with extended fields."""

    class Role(models.TextChoices):
        """User roles for RBAC."""

        SUPER_ADMIN = "SUPER_ADMIN", _("Super Admin")
        ADMINISTRATOR = "ADMINISTRATOR", _("Administrator")
        WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER", _("Warehouse Manager")
        WAREHOUSE_OPERATOR = "WAREHOUSE_OPERATOR", _("Warehouse Operator")
        MAINTENANCE_MANAGER = "MAINTENANCE_MANAGER", _("Maintenance Manager")
        TECHNICIAN = "TECHNICIAN", _("Technician")
        VIEWER = "VIEWER", _("Viewer")

    class Status(models.TextChoices):
        """User account status."""

        PENDING = "PENDING", _("Pending")
        ACTIVE = "ACTIVE", _("Active")
        SUSPENDED = "SUSPENDED", _("Suspended")
        DEACTIVATED = "DEACTIVATED", _("Deactivated")

    # Basic information
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone = models.CharField(_("phone number"), max_length=20, validators=[PhoneValidator()], blank=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)

    # Employee information
    employee_id = models.CharField(
        _("employee ID"),
        max_length=20,
        unique=True,
        validators=[EmployeeIDValidator()],
        db_index=True,
    )
    department = models.CharField(_("department"), max_length=100, blank=True)
    position = models.CharField(_("position"), max_length=100, blank=True)

    # Role and status
    role = models.CharField(_("role"), max_length=30, choices=Role.choices, default=Role.VIEWER)
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    # Invitation and activation
    invitation_token = models.UUIDField(_("invitation token"), default=uuid.uuid4, editable=False, blank=True, null=True)
    invitation_sent_at = models.DateTimeField(_("invitation sent at"), null=True, blank=True)
    invitation_accepted_at = models.DateTimeField(_("invitation accepted at"), null=True, blank=True)
    terms_accepted = models.BooleanField(_("terms accepted"), default=False)
    terms_accepted_at = models.DateTimeField(_("terms accepted at"), null=True, blank=True)

    # Tracking
    last_login = models.DateTimeField(_("last login"), null=True, blank=True)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "employee_id"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["employee_id"]),
            models.Index(fields=["role"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self) -> str:
        """Return full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        """Return short name."""
        return self.first_name

    def has_role(self, *roles: str) -> bool:
        """Check if user has any of the specified roles."""
        return self.role in roles

    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role in [self.Role.SUPER_ADMIN, self.Role.ADMINISTRATOR]

    def is_warehouse_manager(self) -> bool:
        """Check if user is warehouse manager."""
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ADMINISTRATOR,
            self.Role.WAREHOUSE_MANAGER,
        ]

    def is_maintenance_manager(self) -> bool:
        """Check if user is maintenance manager."""
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ADMINISTRATOR,
            self.Role.MAINTENANCE_MANAGER,
        ]

    def activate_account(self) -> None:
        """Activate user account."""
        self.status = self.Status.ACTIVE
        self.is_active = True
        self.invitation_accepted_at = timezone.now()
        self.save()

    def deactivate_account(self) -> None:
        """Deactivate user account."""
        self.status = self.Status.DEACTIVATED
        self.is_active = False
        self.save()

    def suspend_account(self) -> None:
        """Suspend user account."""
        self.status = self.Status.SUSPENDED
        self.is_active = False
        self.save()

    def regenerate_invitation_token(self) -> str:
        """Regenerate invitation token."""
        self.invitation_token = uuid.uuid4()
        self.invitation_sent_at = timezone.now()
        self.invitation_accepted_at = None
        self.terms_accepted = False
        self.terms_accepted_at = None
        self.save()
        return str(self.invitation_token)


class Permission(models.Model):
    """Custom permission model for granular access control."""

    name = models.CharField(_("name"), max_length=100, unique=True)
    codename = models.CharField(_("codename"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)
    module = models.CharField(_("module"), max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        ordering = ["module", "name"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.module}.{self.codename}" if self.module else self.codename


class RolePermission(models.Model):
    """Role to permission mapping."""

    role = models.CharField(_("role"), max_length=30, choices=User.Role.choices)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="role_permissions")
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("role permission")
        verbose_name_plural = _("role permissions")
        unique_together = ["role", "permission"]
        ordering = ["role", "permission"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.role} - {self.permission.codename}"


class LoginHistory(models.Model):
    """Track user login history."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_histories")
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.TextField(_("user agent"), blank=True)
    login_time = models.DateTimeField(_("login time"), auto_now_add=True)
    logout_time = models.DateTimeField(_("logout time"), null=True, blank=True)
    status = models.CharField(_("status"), max_length=20, default="SUCCESS")

    class Meta:
        verbose_name = _("login history")
        verbose_name_plural = _("login histories")
        ordering = ["-login_time"]

    def __str__(self) -> str:
        """String representation."""
        return f"{self.user.email} - {self.login_time}"
