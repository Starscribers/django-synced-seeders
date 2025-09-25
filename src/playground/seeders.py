from seeds import Seeder, seeder_registry

from .models import ExamplePresetModel


@seeder_registry.register()
class ExamplePresetSeeder(Seeder):
    """An example seeder that creates preset data."""

    seed_slug = "example_preset"
    exporting_querysets = (ExamplePresetModel.objects.all(),)
