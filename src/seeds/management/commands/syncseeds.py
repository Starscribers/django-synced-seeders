from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand
from typing_extensions import Self

from seeds import seeder_registry
from seeds.models import SeedRevision
from seeds.utils import get_seed_meta_path

if TYPE_CHECKING:
    from argparse import ArgumentParser


class Command(BaseCommand):
    """
    Syncs seeds from registered seeders.
    """

    def add_arguments(self: Self, parser: ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "tags",
            nargs="*",
            type=str,
            help="Optional tags to filter seeders. If provided, only seeders with matching tags will be synced.",
        )

    def handle(self: Self, *args: tuple, **kwargs: dict[str, Any]) -> None:
        tags_raw: Any = kwargs.get("tags", [])
        tags: list[str] = tags_raw if isinstance(tags_raw, list) else []
        self.stdout.write("[Synced Seeders] Syncing seeds...")

        # Filter seeders by tags if provided
        if tags:
            seeders_to_sync = seeder_registry.get_by_tags(tags)
            self.stdout.write(
                f"[Synced Seeders] Filtering by tags: {', '.join(tags)}",
            )
        else:
            seeders_to_sync = seeder_registry.registry

        new_seeds_loaded = 0
        meta_file = get_seed_meta_path()
        data = json.load(meta_file.open("r"))

        for seed_slug, seeder in seeders_to_sync.items():
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
