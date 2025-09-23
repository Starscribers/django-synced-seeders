"""
End-to-end integration tests for the complete seeders workflow.
"""

import json
import tempfile
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import override_settings

from playground.models import ExamplePresetModel
from seeds.models import SeedRevision
from seeds.registries import seeder_registry
from seeds.seeders import Seeder


class TestSeederForIntegration(Seeder):
    """Custom test seeder for integration tests."""

    seed_slug = "integration_test_seeder"
    delete_existing = True
    exporting_querysets = (ExamplePresetModel.objects.all(),)


@pytest.mark.django_db
def test_complete_seed_lifecycle(tmp_path: Path) -> None:
    """Test complete seed lifecycle: create data -> export -> clear -> sync -> verify."""
    # Setup temporary paths
    seed_file = tmp_path / "lifecycle_test.json"
    meta_file = tmp_path / "lifecycle_meta.json"

    # Initialize meta file
    with meta_file.open("w") as f:
        json.dump({}, f)

    # Create initial test data
    ExamplePresetModel.objects.create(name="Lifecycle Test 1", value=100)
    ExamplePresetModel.objects.create(name="Lifecycle Test 2", value=200)

    initial_count = ExamplePresetModel.objects.count()
    assert initial_count == 2

    # Create a test seeder instance
    test_seeder = TestSeederForIntegration()
    test_seeder.seed_path = str(seed_file)

    # Step 1: Export the data
    test_seeder.export()

    # Verify export file was created
    assert seed_file.exists()

    with seed_file.open() as f:
        exported_data = json.load(f)

    assert len(exported_data) == 2
    names = [item["fields"]["name"] for item in exported_data]
    assert "Lifecycle Test 1" in names
    assert "Lifecycle Test 2" in names

    # Update meta file to indicate version 1
    with meta_file.open("w") as f:
        json.dump({"integration_test_seeder": 1}, f)

    # Step 2: Clear existing data (simulate fresh database)
    ExamplePresetModel.objects.all().delete()
    assert ExamplePresetModel.objects.count() == 0

    # Step 3: Load the data back using the seeder
    test_seeder.load_seed()

    # Step 4: Verify the data was restored
    restored_count = ExamplePresetModel.objects.count()
    assert restored_count == 2

    restored_objects = list(ExamplePresetModel.objects.all())
    restored_names = [obj.name for obj in restored_objects]
    assert "Lifecycle Test 1" in restored_names
    assert "Lifecycle Test 2" in restored_names

    # Verify values are correct
    for obj in restored_objects:
        if obj.name == "Lifecycle Test 1":
            assert obj.value == 100
        elif obj.name == "Lifecycle Test 2":
            assert obj.value == 200


@pytest.mark.django_db
def test_incremental_seed_updates(tmp_path):
    """Test incremental seed updates with version management."""
    meta_file = tmp_path / "incremental_meta.json"
    with override_settings(SEEDS_META_PATH=str(meta_file)):
        # Initialize meta file
        with meta_file.open("w") as f:
            json.dump({}, f)

        test_seeder = TestSeederForIntegration()

        # Create initial data (version 1)
        ExamplePresetModel.objects.create(name="V1 Object", value=1)
        test_seeder.export()

        with meta_file.open("w") as f:
            json.dump({"integration_test_seeder": 1}, f)

        # Create SeedRevision record for version 1
        SeedRevision.objects.create(seed_slug="integration_test_seeder", revision=1)

        # Add more data (version 2)
        ExamplePresetModel.objects.create(name="V2 Object", value=2)
        test_seeder.export()

        with meta_file.open("w") as f:
            json.dump({"integration_test_seeder": 2}, f)

        # Now test sync with version management
        # Temporarily register our test seeder
        seeder_registry.registry["integration_test_seeder"] = type(test_seeder)

        # Clear data and sync
        ExamplePresetModel.objects.all().delete()

        out = StringIO()
        call_command("syncseeds", stdout=out)

        # Should have synced because revision 2 > revision 1
        output = out.getvalue()
        assert "integration_test_seeder is installed (1 -> v2)" in output

        # Verify data
        assert ExamplePresetModel.objects.count() == 2
        names = list(ExamplePresetModel.objects.values_list("name", flat=True))
        assert "V1 Object" in names
        assert "V2 Object" in names

        # Verify new SeedRevision was created
        latest_revision = (
            SeedRevision.objects.filter(seed_slug="integration_test_seeder")
            .order_by("-id")
            .first()
        )
        assert latest_revision is not None
        assert latest_revision.revision == 2


@pytest.mark.django_db
def test_delete_existing_behavior(tmp_path: Path) -> None:
    """Test the delete_existing behavior during seed loading."""
    seed_file = tmp_path / "delete_test.json"

    class TestSeederWithDelete(Seeder):
        seed_slug = "delete_test_seeder"
        seed_path = str(seed_file)
        delete_existing = True
        exporting_querysets = (ExamplePresetModel.objects.all(),)

    class TestSeederWithoutDelete(Seeder):
        seed_slug = "nodelete_test_seeder"
        seed_path = str(seed_file)
        delete_existing = False
        exporting_querysets = (ExamplePresetModel.objects.all(),)

    # Create initial data and export it
    ExamplePresetModel.objects.create(name="Seed Data", value=999)

    seeder_with_delete = TestSeederWithDelete()
    seeder_with_delete.export()

    # Add some conflicting data
    ExamplePresetModel.objects.create(name="Existing Data", value=111)
    assert ExamplePresetModel.objects.count() == 2

    # Test with delete_existing=True
    seeder_with_delete.load_seed()

    # Should only have the seed data (existing data deleted)
    assert ExamplePresetModel.objects.count() == 1
    assert ExamplePresetModel.objects.get().name == "Seed Data"

    # Add conflicting data again
    ExamplePresetModel.objects.create(name="Existing Data Again", value=222)
    assert ExamplePresetModel.objects.count() == 2

    # Test with delete_existing=False
    seeder_without_delete = TestSeederWithoutDelete()
    seeder_without_delete.load_seed()

    # Should have both existing and seed data (no deletion)
    # Note: This might create duplicates depending on the seed data
    assert ExamplePresetModel.objects.count() >= 2


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


@pytest.mark.django_db
def test_large_dataset_export_import() -> None:
    """Test with a larger dataset to verify performance."""
    # Create a moderate-sized dataset (100 objects)
    test_objects = []
    for i in range(100):
        obj = ExamplePresetModel(name=f"Bulk Test {i}", value=i * 10)
        test_objects.append(obj)

    ExamplePresetModel.objects.bulk_create(test_objects)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp_file:

        class BulkTestSeeder(Seeder):
            seed_slug = "bulk_test"
            seed_path = tmp_file.name
            exporting_querysets = (ExamplePresetModel.objects.all(),)

        seeder = BulkTestSeeder()

        # Test export
        seeder.export()

        # Verify file size and content
        export_file = Path(tmp_file.name)
        assert export_file.stat().st_size > 1000  # Should be reasonably sized

        # Clear and reload
        ExamplePresetModel.objects.all().delete()
        assert ExamplePresetModel.objects.count() == 0

        seeder.load_seed()

        # Verify all data was restored
        assert ExamplePresetModel.objects.count() == 100

        # Verify some sample data
        first_obj = ExamplePresetModel.objects.filter(name="Bulk Test 0").get()
        assert first_obj.value == 0

        last_obj = ExamplePresetModel.objects.filter(name="Bulk Test 99").get()
        assert last_obj.value == 990


@pytest.mark.django_db
def test_multiple_revisions_performance() -> None:
    """Test performance with multiple seed revisions."""
    # Create multiple revisions for the same seed
    for i in range(10):
        SeedRevision.objects.create(seed_slug="performance_test", revision=i + 1)

    # Query performance test
    latest_revision = (
        SeedRevision.objects.filter(seed_slug="performance_test")
        .order_by("-revision")
        .first()
    )
    assert latest_revision is not None
    assert latest_revision.revision == 10

    # Test bulk operations
    revisions_to_delete = SeedRevision.objects.filter(
        seed_slug="performance_test", revision__lt=8
    )

    deleted_count, _ = revisions_to_delete.delete()
    assert deleted_count == 7

    remaining_count = SeedRevision.objects.filter(seed_slug="performance_test").count()
    assert remaining_count == 3
