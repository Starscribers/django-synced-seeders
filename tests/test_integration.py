"""
End-to-end integration tests for the complete seeders workflow.
"""

import tempfile
from pathlib import Path

import pytest

from playground.models import ExamplePresetModel
from seeds import Seeder, seeder_registry


@pytest.mark.django_db
def test_missing_seed_file_handling() -> None:
    """Test handling of missing seed files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        non_existent_file = Path(tmp_dir) / "missing.json"

        class TestSeederMissing(Seeder):
            seed_slug = "missing_test"
            seed_path = str(non_existent_file)
            exporting_querysets = (ExamplePresetModel.objects.all(),)

        seeder = TestSeederMissing()

        # Loading a missing file should raise an error via Django's loaddata
        from django.core.management.base import CommandError

        with pytest.raises(CommandError):
            seeder.load_seed()


@pytest.mark.django_db
def test_permission_error_handling() -> None:
    """Test handling of permission errors during export."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        readonly_file = Path(tmp_dir) / "readonly.json"
        readonly_file.touch()
        readonly_file.chmod(0o444)  # Read-only

        class TestSeederReadonly(Seeder):
            seed_slug = "readonly_test"
            seed_path = str(readonly_file)
            exporting_querysets = (ExamplePresetModel.objects.all(),)

        # Create some data to export
        ExamplePresetModel.objects.create(name="Test", value=1)

        seeder = TestSeederReadonly()

        # Should raise permission error when trying to write
        with pytest.raises(PermissionError):
            seeder.export()


def test_seeder_discovery():
    """Test that seeders are auto-discovered and registered."""
    seeder_class = seeder_registry.get("auto-imported-seeder")
    assert seeder_class is not None
    assert issubclass(seeder_class, Seeder)
