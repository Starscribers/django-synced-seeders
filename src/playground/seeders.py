from seeds import Seeder, seeder_registry

from .models import ExamplePresetModel


@seeder_registry.register()
class ExamplePresetSeeder(Seeder):
    """An example seeder that creates preset data."""

    seed_slug = "example_preset"
    priority = 100  # Default priority
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags="e2e")
class E2ESeeder(Seeder):
    """Seeder for E2E testing scenarios."""

    seed_slug = "e2e_data"
    priority = 100  # Default priority
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags=["development", "demo"])
class DemoSeeder(Seeder):
    """Seeder for development and demo purposes.

    Note: If this seeder had dependencies on foreign keys from other models,
    you would set a higher priority number (e.g., priority = 50 for dependencies,
    priority = 100 for this seeder).
    """

    seed_slug = "demo_data"
    priority = 100  # Default priority
    exporting_querysets = (ExamplePresetModel.objects.all(),)
