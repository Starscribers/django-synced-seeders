"""
URL configuration for example_project project.
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
]
