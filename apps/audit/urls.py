"""
URL configuration for audit app.
"""

from django.urls import path

from apps.audit.views import (
    AuditLogArchiveListView,
    AuditLogByEntityView,
    AuditLogByUserView,
    AuditLogDetailView,
    AuditLogListView,
    AuditLogRecentView,
)

app_name = "audit"

urlpatterns = [
    path("", AuditLogListView.as_view(), name="audit_log_list"),
    path("<uuid:id>/", AuditLogDetailView.as_view(), name="audit_log_detail"),
    path("user/<uuid:user_id>/", AuditLogByUserView.as_view(), name="audit_log_by_user"),
    path("entity/<str:entity_type>/<uuid:entity_id>/", AuditLogByEntityView.as_view(), name="audit_log_by_entity"),
    path("recent/<int:days>/", AuditLogRecentView.as_view(), name="audit_log_recent"),
    path("archive/", AuditLogArchiveListView.as_view(), name="audit_log_archive"),
]
