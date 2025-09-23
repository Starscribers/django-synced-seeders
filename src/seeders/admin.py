from __future__ import annotations

from django.contrib import admin

from .models import (
    SeedRevision,
)


@admin.register(SeedRevision)
class SeedRevisionAdmin(admin.ModelAdmin):
    list_display = ("seed_slug", "revision", "created_at", "updated_at")
    list_filter = ("seed_slug",)
    search_fields = ("seed_slug",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
