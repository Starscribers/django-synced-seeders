from __future__ import annotations

from typing import TYPE_CHECKING

from any_registries import Registry

from .seeders import Seeder

if TYPE_CHECKING:
    from collections.abc import Callable


class TaggedRegistry(Registry):
    """Registry that supports tagging seeders."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tags = {}

    def register(
        self,
        key: str | None = None,
        tags: list[str] | str | None = None,
    ) -> Callable:
        """Register a seeder with optional tags.

        Args:
            key: Optional key for registration
            tags: Optional tag or list of tags for the seeder

        Returns:
            Decorator function
        """

        def registry(target: type[Seeder]) -> type[Seeder]:
            # Store tags on the seeder class
            if tags is not None:
                tag_list = [tags] if isinstance(tags, str) else tags
                target.tags = tag_list

                # Register the key for each tag
                actual_key = key if key is not None else self.key_getter(target)
                for tag in tag_list:
                    if tag not in self._tags:
                        self._tags[tag] = []
                    self._tags[tag].append(actual_key)

            # Call parent register
            if key is None:
                if self.key_getter is None:
                    msg = "A key or key_getter must be provided for registration."
                    raise ValueError(msg)
                self._registry[self.key_getter(target)] = target
            else:
                self._registry[key] = target
            return target

        return registry

    def get_by_tags(self, tags: list[str] | str) -> dict[str, type[Seeder]]:
        """Get all seeders that match any of the given tags.

        Args:
            tags: Tag or list of tags to filter by

        Returns:
            Dictionary of seed_slug to Seeder class for matching seeders
        """
        tag_list = [tags] if isinstance(tags, str) else tags
        matching_keys = set()

        for tag in tag_list:
            if tag in self._tags:
                matching_keys.update(self._tags[tag])

        return {key: self._registry[key] for key in matching_keys if key in self._registry}


seeder_registry: TaggedRegistry = TaggedRegistry(
    key=lambda seeder_cls: seeder_cls.seed_slug
).auto_load("*/seeders.py")
