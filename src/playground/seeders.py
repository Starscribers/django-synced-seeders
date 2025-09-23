from seeds.registries import seeder_registry
from seeds.seeders import Seeder

from .models import ExamplePresetModel


@seeder_registry.register()
class ExamplePresetSeeder(Seeder):
    """An example seeder that creates preset data."""

    seed_slug = "example_preset"
    exporting_querysets = (ExamplePresetModel.objects.all(),)
