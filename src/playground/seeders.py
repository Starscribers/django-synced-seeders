from seeds import Seeder, seeder_registry

from .models import ExamplePresetModel


@seeder_registry.register()
class ExamplePresetSeeder(Seeder):
    """An example seeder that creates preset data."""

    seed_slug = "example_preset"
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags="e2e")
class E2ESeeder(Seeder):
    """Seeder for E2E testing scenarios."""

    seed_slug = "e2e_data"
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@seeder_registry.register(tags=["development", "demo"])
class DemoSeeder(Seeder):
    """Seeder for development and demo purposes."""

    seed_slug = "demo_data"
    exporting_querysets = (ExamplePresetModel.objects.all(),)
