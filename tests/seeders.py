"""
This file is usually not discovered by Python, this file exists to ensure
that all `<app>/seeds.py` files are imported by seeder_registry and all seeders are registered.
"""

from playground.models import ExamplePresetModel
from seeds import Seeder, seeder_registry


# Register seeders
@seeder_registry.register()
class ExamplePresetSeeder(Seeder):
    """Seeder for ExamplePresetModel."""

    seed_slug = "auto-imported-seeder"
    delete_existing = True
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags="e2e")
class E2ETestSeeder(Seeder):
    """Seeder for E2E tests."""

    seed_slug = "e2e-test-seeder"
    delete_existing = True
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags=["integration", "e2e"])
class IntegrationTestSeeder(Seeder):
    """Seeder for integration tests."""

    seed_slug = "integration-test-seeder"
    delete_existing = True
    exporting_querysets = (ExamplePresetModel.objects.all(),)
