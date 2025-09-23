from __future__ import annotations

import json

from django.core.management.base import BaseCommand, CommandParser
from typing_extensions import Self

from seeds.registries import seeder_registry
from seeds.utils import get_seed_meta_path


class Command(BaseCommand):
    """
    Flushes the API Gateway stage cache.
    """

    def add_arguments(self: Self, parser: CommandParser) -> None:
        parser.add_argument(
            "seed_slug",
            type=str,
            help="Force sync all seeds.",
        )
        super().add_arguments(parser)

    def handle(self: Self, seed_slug: str, *args: tuple, **kwargs: dict) -> None:
        seed_manager = seeder_registry.registry[seed_slug]

        self.stdout.write("[Synced Seeders] Exporting seeds...")
        seed_manager().export()

        self.stdout.write(f"[Synced Seeders] Fixture {seed_slug} is exported.")
        meta_file = get_seed_meta_path()

        data = json.load(meta_file.open("r"))
        revision = data[seed_slug] = data.get(seed_slug, 0) + 1

        with meta_file.open("w") as file:
            json.dump(data, file, indent=4)
            file.write("\n")

        self.stdout.write(
            f"[Synced Seeders] Updated seed to revision {revision}.",
        )
