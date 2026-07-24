"""
URL configuration for notifications app.
"""

from django.urls import path

from apps.notifications.views import MyNotificationsView, NotificationDetailView, NotificationListView

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("<uuid:id>/", NotificationDetailView.as_view(), name="notification_detail"),
    path("my/", MyNotificationsView.as_view(), name="my_notifications"),
]
