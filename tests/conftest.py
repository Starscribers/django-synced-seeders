"""
Pytest configuration and shared fixtures for seeders tests.
"""

import tempfile
from pathlib import Path

import django
import pytest


def pytest_configure(config):
    """Configure Django for pytest."""
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()


@pytest.fixture
def temp_seed_file():
    """Provide a temporary seed file for tests."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp_file:
        yield Path(tmp_file.name)
    # File is automatically cleaned up


@pytest.fixture
def temp_meta_file():
    """Provide a temporary meta file for tests."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as tmp_file:
        yield Path(tmp_file.name)
    # File is automatically cleaned up


@pytest.fixture
def temp_directory():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_seed_data():
    """Provide sample seed data for tests."""
    return [
        {
            "model": "playground.examplepresetmodel",
            "pk": 1,
            "fields": {"name": "Test Object 1", "value": 100},
        },
        {
            "model": "playground.examplepresetmodel",
            "pk": 2,
            "fields": {"name": "Test Object 2", "value": 200},
        },
    ]


@pytest.fixture
def sample_meta_data():
    """Provide sample meta data for tests."""
    return {"example_preset": 1, "test_seeder": 2, "another_seeder": 5}


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Give all tests access to the database.

    This fixture is autouse=True, which means it's automatically used
    for all tests. This is useful for django-synced-seeds since most
    functionality involves database operations.
    """
    pass


@pytest.fixture
def clean_seed_revisions():
    """Clean up SeedRevision records before and after tests."""
    from seeds.models import SeedRevision

    # Clean up before test
    SeedRevision.objects.all().delete()

    yield

    # Clean up after test
    SeedRevision.objects.all().delete()


@pytest.fixture
def clean_example_models():
    """Clean up ExamplePresetModel records before and after tests."""
    from playground.models import ExamplePresetModel

    # Clean up before test
    ExamplePresetModel.objects.all().delete()

    yield

    # Clean up after test
    ExamplePresetModel.objects.all().delete()


@pytest.fixture
def isolated_registry():
    """Provide a clean seeder registry for tests."""
    from seeds.registries import seeder_registry

    # Store original registry
    original_registry = seeder_registry.registry.copy()

    yield seeder_registry

    # Restore original registry
    seeder_registry.registry = original_registry


# Pytest markers for organizing tests
pytest_plugins = []
