from django.db import models
from typing_extensions import Self


class SeedRevision(models.Model):
    """
    Model to track which seed versions have been loaded.

    This prevents duplicate loading of the same seed version
    and enables incremental seed updates.
    """

    seed_slug: models.CharField = models.CharField(
        max_length=255,
        help_text="Unique identifier for the seed",
    )
    revision: models.IntegerField = models.IntegerField(
        help_text="Version number of the loaded seed",
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "django_seed_manager_revision"
        verbose_name = "seed Revision"
        verbose_name_plural = "seed Revisions"
        indexes = [
            models.Index(fields=["seed_slug"]),
            models.Index(fields=["seed_slug", "revision"]),
        ]

    def __str__(self: Self) -> str:
        return f"{self.seed_slug} - v{self.revision}"
