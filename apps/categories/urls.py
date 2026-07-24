"""
URL configuration for categories app.
"""

from django.urls import path
from rest_framework_nested import routers

from apps.categories.views import CategoryDetailView, CategoryListView, CategoryTreeView

app_name = "categories"

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("tree/", CategoryTreeView.as_view(), name="category_tree"),
    path("<uuid:id>/", CategoryDetailView.as_view(), name="category_detail"),
]
