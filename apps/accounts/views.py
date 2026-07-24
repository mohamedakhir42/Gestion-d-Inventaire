"""
API views for accounts app.
"""

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.models import LoginHistory, Permission, RolePermission, User
from apps.accounts.permissions import CanInviteUsers, CanManageUsers, IsOwnerOrAdmin
from apps.accounts.serializers import (
    CustomTokenObtainPairSerializer,
    LoginHistorySerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PermissionSerializer,
    RolePermissionSerializer,
    TokenRefreshSerializer,
    UserActivationSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.accounts.services import AuthService, PermissionService, UserService
from apps.accounts.selectors import LoginHistorySelector, UserSelector
from common.exceptions import NotFoundError, ValidationError
from common.mixins import AuditMixin
from common.permissions import IsActiveUser

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view."""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Any, *args, **kwargs) -> Response:
        """Handle login and create login history."""
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            auth_service = AuthService()
            auth_service.create_login_history(request.user, request)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view."""

    serializer_class = TokenRefreshSerializer


class LogoutView(generics.GenericAPIView):
    """Logout view."""

    permission_classes = [IsAuthenticated, IsActiveUser]

    def post(self, request: Any) -> Response:
        """Handle logout."""
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            auth_service = AuthService()
            auth_service.logout_user(request.user, request)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListCreateAPIView):
    """List and create users."""

    permission_classes = [IsAuthenticated, IsActiveUser, CanManageUsers]
    serializer_class = UserSerializer
    filterset_fields = ["role", "status", "department"]
    search_fields = ["first_name", "last_name", "email", "employee_id"]
    ordering_fields = ["created_at", "last_login", "first_name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Get user queryset."""
        selector = UserSelector()
        return selector.get_all()

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """Create user with invitation."""
        user_service = UserService()
        user = user_service.invite_user(serializer.validated_data, self.request.user)
        return user


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a user."""

    permission_classes = [IsAuthenticated, IsActiveUser, IsOwnerOrAdmin]
    queryset = User.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        """Get appropriate serializer."""
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer

    def perform_update(self, serializer):
        """Update user."""
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """Soft delete user."""
        user_service = UserService()
        user_service.deactivate_user(instance, self.request.user)


class MeView(generics.RetrieveUpdateAPIView):
    """Current user profile view."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = UserSerializer

    def get_object(self):
        """Get current user."""
        return self.request.user


class ActivateAccountView(generics.GenericAPIView):
    """Activate account with invitation token."""

    permission_classes = [AllowAny]
    serializer_class = UserActivationSerializer

    def post(self, request: Any) -> Response:
        """Activate account."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        user = user_service.activate_user(
            token=str(serializer.validated_data["token"]),
            password=serializer.validated_data["password"],
            avatar=serializer.validated_data.get("avatar"),
        )

        return Response(
            {"detail": "Account activated successfully.", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class PasswordChangeView(generics.GenericAPIView):
    """Change password for authenticated user."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = PasswordChangeSerializer

    def post(self, request: Any) -> Response:
        """Change password."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        user_service.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    """Request password reset."""

    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request: Any) -> Response:
        """Request password reset."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        # Generate password reset token
        uid = urlsafe_base64_encode(force_str(user.pk).encode())
        token = default_token_generator.make_token(user)

        # TODO: Send email with reset link
        # This will be handled by the notification service

        return Response(
            {"detail": "Password reset email sent if user exists."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """Confirm password reset."""

    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request: Any) -> Response:
        """Confirm password reset."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(request.data.get("uid", "")))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, serializer.validated_data["token"]):
                raise ValidationError("Invalid or expired token.")

            user_service = UserService()
            user_service.reset_password(user, serializer.validated_data["new_password"])

            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)

        except (User.DoesNotExist, ValueError):
            raise ValidationError("Invalid reset link.")


class ResendInvitationView(generics.GenericAPIView):
    """Resend invitation email."""

    permission_classes = [IsAuthenticated, IsActiveUser, CanInviteUsers]

    def post(self, request: Any, id: str) -> Response:
        """Resend invitation."""
        try:
            user = User.objects.get(id=id)
            user_service = UserService()
            token = user_service.resend_invitation(user)

            # TODO: Send email with new invitation link
            # This will be handled by the notification service

            return Response({"detail": "Invitation resent successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFoundError("User not found.")


class UserActionView(generics.GenericAPIView):
    """Perform actions on user (suspend, restore, etc.)."""

    permission_classes = [IsAuthenticated, IsActiveUser, CanManageUsers]

    def post(self, request: Any, id: str, action: str) -> Response:
        """Perform action on user."""
        try:
            user = User.objects.get(id=id)
            user_service = UserService()

            if action == "suspend":
                user_service.suspend_user(user, request.user)
            elif action == "restore":
                user_service.restore_user(user, request.user)
            else:
                raise ValidationError("Invalid action.")

            return Response({"detail": f"User {action}ed successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFoundError("User not found.")


class PermissionListView(generics.ListAPIView):
    """List all permissions."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = PermissionSerializer
    filterset_fields = ["module"]
    ordering = ["module", "name"]

    def get_queryset(self):
        """Get permission queryset."""
        return Permission.objects.all()


class RolePermissionListView(generics.ListAPIView):
    """List permissions for a role."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = RolePermissionSerializer

    def get_queryset(self):
        """Get role permissions."""
        role = self.kwargs.get("role")
        return RolePermission.objects.filter(role=role)


class LoginHistoryListView(generics.ListAPIView):
    """List login history."""

    permission_classes = [IsAuthenticated, IsActiveUser]
    serializer_class = LoginHistorySerializer
    ordering = ["-login_time"]

    def get_queryset(self):
        """Get login history."""
        user_id = self.kwargs.get("user_id")
        selector = LoginHistorySelector()
        if user_id:
            user = User.objects.get(id=user_id)
            if not (self.request.user.is_admin() or self.request.user.id == user.id):
                self.permission_denied(self.request)
            return selector.get_user_login_history(user)
        return selector.get_recent_logins()
