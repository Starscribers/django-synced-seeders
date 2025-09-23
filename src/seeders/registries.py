from __future__ import annotations

from any_registries import Registry

from .seeders import Seeder

seeder_registry: Registry[str, type[Seeder]] = Registry(
    key=lambda seeder_cls: seeder_cls.seed_slug
).auto_load("*/seeders.py")
