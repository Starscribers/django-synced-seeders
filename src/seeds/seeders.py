from __future__ import annotations

import json
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from django.core import serializers
from django.core.management import call_command
from typing_extensions import Self

from seeds.utils import get_seed_meta_path

if TYPE_CHECKING:
    from collections.abc import Iterable


from typing import TYPE_CHECKING


class Seeder:
    """
    Base class for managing Django seeds.

    Provides functionality for loading seeds, exporting database objects
    to seeds, and managing seed metadata.
    """

    # Path to the seed file (relative to Django project root)
    seed_path: Path | str | None = None

    # Unique slug identifier for the seed
    seed_slug: str = "base-seed"

    # Whether to delete existing objects before loading
    delete_existing: bool = True

    # Tuple of querysets to export when creating seeds
    exporting_querysets: tuple = ()

    def __init__(self: Self) -> None:
        self.seed_path = (
            self.seed_path
            or get_seed_meta_path().parent / f"seeds/{self.seed_slug}.json"
        )

    def load_seed(self: Self) -> None:
        """
        Load the seed into the database.

        If delete_existing is True, will delete all objects from
        exporting_querysets before loading the seed.
        """
        if self.delete_existing:
            for queryset in self.exporting_querysets:
                queryset.delete()

        if self.seed_path:
            call_command("loaddata", self.seed_path)
        else:
            # Import here to avoid circular imports during package setup
            import logging

            logger = logging.getLogger(__name__)
            logger.error("Seed path is not set.")

    def get_export_objects(self: Self) -> Iterable:
        """
        Get all objects to export as an iterable.

        Returns:
            Iterable of Django model instances from all exporting_querysets
        """
        return chain(*[queryset.all() for queryset in self.exporting_querysets])

    def export(self: Self) -> None:
        """
        Export database objects to a seed file.

        Serializes all objects from exporting_querysets to JSON format
        and writes them to the seed_path.
        """
        if not self.seed_path:
            msg = "Seed path is not set."
            raise ValueError(msg)

        seed_file = Path(self.seed_path)
        seed_file.parent.mkdir(parents=True, exist_ok=True)

        with seed_file.open("w", encoding="utf8") as f:
            f.write(
                json.dumps(
                    json.loads(
                        serializers.serialize("json", self.get_export_objects()),
                    ),
                    indent=4,
                    ensure_ascii=False,
                )
                + "\n",
            )
