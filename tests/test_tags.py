"""Tests for seeder tag functionality."""

from __future__ import annotations

import pytest


@pytest.fixture
def registry():
    """Get the seeder registry with all seeders loaded."""
    # Force re-import of test seeders to ensure tags are registered
    import tests.seeders  # noqa: F401
    from seeds import seeder_registry

    return seeder_registry


def test_register_with_single_tag(registry):
    """Test that seeders can be registered with a single tag."""
    # Check that E2E seeder is registered with 'e2e' tag
    e2e_seeders = registry.get_by_tags("e2e")
    assert "e2e-test-seeder" in e2e_seeders
    assert "integration-test-seeder" in e2e_seeders


def test_register_with_multiple_tags(registry):
    """Test that seeders can be registered with multiple tags."""
    # Check that integration seeder is registered with both tags
    integration_seeders = registry.get_by_tags("integration")
    assert "integration-test-seeder" in integration_seeders

    e2e_seeders = registry.get_by_tags("e2e")
    assert "integration-test-seeder" in e2e_seeders


def test_get_by_multiple_tags(registry):
    """Test filtering by multiple tags returns union of results."""
    seeders = registry.get_by_tags(["e2e", "integration"])
    assert "e2e-test-seeder" in seeders
    assert "integration-test-seeder" in seeders


def test_get_by_nonexistent_tag(registry):
    """Test that querying for non-existent tag returns empty dict."""
    seeders = registry.get_by_tags("nonexistent")
    assert len(seeders) == 0


def test_untagged_seeder_not_in_tag_query(registry):
    """Test that untagged seeders are not returned in tag queries."""
    e2e_seeders = registry.get_by_tags("e2e")
    assert "auto-imported-seeder" not in e2e_seeders


def test_tags_attribute_set_on_seeder_class(registry):
    """Test that tags are set as attribute on seeder class."""
    seeder_class = registry.registry["e2e-test-seeder"]
    assert hasattr(seeder_class, "tags")
    assert "e2e" in seeder_class.tags

    seeder_class = registry.registry["integration-test-seeder"]
    assert hasattr(seeder_class, "tags")
    assert "integration" in seeder_class.tags
    assert "e2e" in seeder_class.tags
