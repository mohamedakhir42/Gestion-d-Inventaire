"""
URL configuration for accounts app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.accounts.views import (
    ActivateAccountView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LoginHistoryListView,
    LogoutView,
    MeView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    PermissionListView,
    ResendInvitationView,
    RolePermissionListView,
    UserActionView,
    UserDetailView,
    UserListView,
)

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # User management
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<uuid:id>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<uuid:id>/<str:action>/", UserActionView.as_view(), name="user_action"),
    path("users/<uuid:id>/resend-invitation/", ResendInvitationView.as_view(), name="resend_invitation"),
    path("me/", MeView.as_view(), name="me"),
    # Account activation
    path("activate/", ActivateAccountView.as_view(), name="activate_account"),
    # Password management
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # Permissions
    path("permissions/", PermissionListView.as_view(), name="permission_list"),
    path("permissions/<str:role>/", RolePermissionListView.as_view(), name="role_permissions"),
    # Login history
    path("login-history/", LoginHistoryListView.as_view(), name="login_history"),
    path("login-history/<uuid:user_id>/", LoginHistoryListView.as_view(), name="user_login_history"),
]
