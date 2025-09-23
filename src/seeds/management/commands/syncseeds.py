from __future__ import annotations

import json

from django.core.management.base import BaseCommand
from typing_extensions import Self

from seeds.models import SeedRevision
from seeds.registries import seeder_registry
from seeds.utils import get_seed_meta_path


class Command(BaseCommand):
    """
    Flushes the API Gateway stage cache.
    """

    def handle(self: Self, *args: tuple, **kwargs: dict) -> None:
        self.stdout.write("[Synced Seeders] Syncing seeds...")
        new_seeds_loaded = 0
        meta_file = get_seed_meta_path()
        data = json.load(meta_file.open("r"))

        for seed_slug, seeder in seeder_registry.registry.items():
            seed_revision = data.get(seed_slug, 0)
            original_revision_object = (
                SeedRevision.objects.filter(
                    seed_slug=seed_slug,
                )
                .order_by("-id")
                .first()
            )

            original_revision = (
                original_revision_object.revision
                if original_revision_object
                else "Not installed"
            )
            if original_revision == seed_revision:
                self.stdout.write(
                    f"[Synced Seeders] Fixture {seed_slug} is already synced, skipped.",
                )
                continue
            seeder().load_seed()

            SeedRevision.objects.create(
                seed_slug=seed_slug,
                revision=seed_revision,
            )
            self.stdout.write(
                f"[Synced Seeders] Fixture {seed_slug} is installed ({original_revision} -> v{seed_revision}).",
            )
            new_seeds_loaded += 1

        self.stdout.write(f"[Synced Seeders] Synced {new_seeds_loaded} seeds.")
