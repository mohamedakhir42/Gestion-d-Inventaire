"""
Serializers for accounts app.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import LoginHistory, Permission, RolePermission, User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "avatar",
            "employee_id",
            "department",
            "position",
            "role",
            "role_display",
            "status",
            "status_display",
            "is_staff",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "last_login", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users (admin only)."""

    password = serializers.CharField(write_only=True, required=False, allow_null=True)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "employee_id",
            "department",
            "position",
            "role",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs: dict) -> dict:
        """Validate input data."""
        if attrs.get("password") and attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"password": _("Passwords do not match.")})
        return attrs

    def create(self, validated_data: dict) -> User:
        """Create user with invitation."""
        validated_data.pop("confirm_password", None)
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
            user.status = User.Status.ACTIVE
        else:
            user.set_unusable_password()
            user.status = User.Status.PENDING
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating users."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "department",
            "position",
            "role",
            "status",
            "avatar",
        ]


class UserActivationSerializer(serializers.Serializer):
    """Serializer for user account activation."""

    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)
    terms_accepted = serializers.BooleanField(required=True)

    def validate(self, attrs: dict) -> dict:
        """Validate activation data."""
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": _("Passwords do not match.")})
        if not attrs["terms_accepted"]:
            raise serializers.ValidationError({"terms_accepted": _("You must accept the terms.")})
        return attrs

    def validate_token(self, value: str) -> str:
        """Validate invitation token."""
        try:
            user = User.objects.get(invitation_token=value, status=User.Status.PENDING)
            if user.invitation_accepted_at:
                raise serializers.ValidationError(_("Invitation already used."))
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Invalid or expired invitation token."))
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        """Validate password change."""
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"new_password": _("Passwords do not match.")})
        return attrs

    def validate_old_password(self, value: str) -> str:
        """Validate old password."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is incorrect."))
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request."""

    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        """Validate email exists."""
        if not User.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError(_("No active user found with this email."))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""

    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        """Validate reset confirmation."""
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"new_password": _("Passwords do not match.")})
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional claims."""

    @classmethod
    def get_token(cls, user: User) -> Any:
        """Add custom claims to token."""
        token = super().get_token(user)
        token["email"] = user.email
        token["full_name"] = user.get_full_name()
        token["role"] = user.role
        token["employee_id"] = user.employee_id
        return token

    def validate(self, attrs: dict) -> dict:
        """Validate and return token data."""
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer for token refresh."""

    refresh = serializers.CharField()


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model."""

    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "description", "module", "created_at"]
        read_only_fields = ["id", "created_at"]


class RolePermissionSerializer(serializers.ModelSerializer):
    """Serializer for RolePermission model."""

    permission_detail = PermissionSerializer(source="permission", read_only=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = RolePermission
        fields = ["id", "role", "role_display", "permission", "permission_detail", "granted_at"]
        read_only_fields = ["id", "granted_at"]


class LoginHistorySerializer(serializers.ModelSerializer):
    """Serializer for LoginHistory model."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = LoginHistory
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "ip_address",
            "user_agent",
            "login_time",
            "logout_time",
            "status",
        ]
        read_only_fields = ["id", "login_time"]
