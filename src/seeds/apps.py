from django.apps import AppConfig


class SyncedSeedsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "seeds"
    verbose_name = "Synced Seeds"
