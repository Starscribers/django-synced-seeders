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
