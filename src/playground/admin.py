from django.contrib import admin

from playground.models import ExamplePresetModel


@admin.register(ExamplePresetModel)
class ExamplePresetModelAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25
