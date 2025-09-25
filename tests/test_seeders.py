"""
End-to-end integration tests for the complete seeders workflow.
"""

import json
from pathlib import Path

import pytest

from playground.models import ExamplePresetModel
from seeds import Seeder


@pytest.mark.django_db
def test_complete_seed_lifecycle(tmp_path: Path) -> None:
    class TestSeederForIntegration(Seeder):
        """Custom test seeder for integration tests."""

        seed_slug = "integration_test_seeder"
        delete_existing = True
        exporting_querysets = (ExamplePresetModel.objects.all(),)

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
