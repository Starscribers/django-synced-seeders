"""
Tests for seeders models.
"""

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from seeds.models import SeedRevision


@pytest.mark.django_db
def test_create_seed_revision():
    """Test creating a SeedRevision instance."""
    revision = SeedRevision.objects.create(seed_slug="test-seed", revision=1)

    assert revision.seed_slug == "test-seed"
    assert revision.revision == 1
    assert revision.created_at is not None
    assert revision.updated_at is not None
    assert revision.created_at <= timezone.now()
    assert revision.updated_at <= timezone.now()


@pytest.mark.django_db
def test_str_method():
    """Test the string representation of SeedRevision."""
    revision = SeedRevision.objects.create(seed_slug="example-seed", revision=5)

    expected_str = "example-seed - v5"
    assert str(revision) == expected_str


@pytest.mark.django_db
def test_seed_slug_max_length():
    """Test that seed_slug respects max_length constraint."""
    # Test valid length
    valid_slug = "a" * 255
    revision = SeedRevision.objects.create(seed_slug=valid_slug, revision=1)
    assert len(revision.seed_slug) == 255

    # Test that longer slugs would fail validation
    invalid_slug = "a" * 256
    revision = SeedRevision(seed_slug=invalid_slug, revision=1)
    with pytest.raises(ValidationError):
        revision.full_clean()


@pytest.mark.django_db
def test_revision_field_accepts_integers():
    """Test that revision field accepts various integer values."""
    # Test positive integer
    revision1 = SeedRevision.objects.create(seed_slug="test1", revision=100)
    assert revision1.revision == 100

    # Test zero
    revision2 = SeedRevision.objects.create(seed_slug="test2", revision=0)
    assert revision2.revision == 0

    # Test negative integer
    revision3 = SeedRevision.objects.create(seed_slug="test3", revision=-1)
    assert revision3.revision == -1


@pytest.mark.django_db
def test_multiple_revisions_same_slug():
    """Test that multiple revisions can exist for the same seed_slug."""
    seed_slug = "multi-revision-seed"

    SeedRevision.objects.create(seed_slug=seed_slug, revision=1)
    SeedRevision.objects.create(seed_slug=seed_slug, revision=2)
    SeedRevision.objects.create(seed_slug=seed_slug, revision=3)

    revisions = SeedRevision.objects.filter(seed_slug=seed_slug)
    assert revisions.count() == 3
    assert set(revisions.values_list("revision", flat=True)) == {1, 2, 3}


@pytest.mark.django_db
def test_same_slug_revision_combination_allowed():
    """Test that same slug-revision combinations are allowed (no unique constraint)."""
    # This tests that there's no unique constraint on (seed_slug, revision)
    SeedRevision.objects.create(seed_slug="duplicate-test", revision=1)
    SeedRevision.objects.create(seed_slug="duplicate-test", revision=1)

    count = SeedRevision.objects.filter(seed_slug="duplicate-test", revision=1).count()
    assert count == 2


@pytest.mark.django_db
def test_auto_timestamps():
    """Test that created_at and updated_at are automatically set."""
    before_creation = timezone.now()

    revision = SeedRevision.objects.create(seed_slug="timestamp-test", revision=1)

    after_creation = timezone.now()

    # Check created_at
    assert before_creation <= revision.created_at <= after_creation

    # Check updated_at
    assert before_creation <= revision.updated_at <= after_creation

    # Initially, created_at and updated_at should be very close
    time_diff = revision.updated_at - revision.created_at
    assert time_diff.total_seconds() < 1


@pytest.mark.django_db
def test_updated_at_changes_on_save():
    """Test that updated_at changes when the object is saved."""
    import time

    revision = SeedRevision.objects.create(seed_slug="update-test", revision=1)
    original_updated_at = revision.updated_at

    # Wait a small amount to ensure timestamp difference
    time.sleep(0.01)

    # Update and save
    revision.revision = 2
    revision.save()

    # Check that updated_at has changed
    assert revision.updated_at > original_updated_at


def test_model_meta_attributes():
    """Test model Meta attributes."""
    meta = SeedRevision._meta

    assert meta.db_table == "django_seed_manager_revision"
    assert meta.verbose_name == "seed Revision"
    assert meta.verbose_name_plural == "seed Revisions"


def test_model_indexes() -> None:
    """Test that proper indexes are defined."""
    meta = SeedRevision._meta

    # Check that indexes exist
    indexes = [index.fields for index in meta.indexes]

    assert ["seed_slug"] in indexes
    assert ["seed_slug", "revision"] in indexes


@pytest.mark.django_db
def test_queryset_operations():
    """Test common queryset operations."""
    # Create test data
    SeedRevision.objects.create(seed_slug="seed-a", revision=1)
    SeedRevision.objects.create(seed_slug="seed-a", revision=2)
    SeedRevision.objects.create(seed_slug="seed-b", revision=1)
    SeedRevision.objects.create(seed_slug="seed-b", revision=3)

    # Test filtering by seed_slug
    seed_a_revisions = SeedRevision.objects.filter(seed_slug="seed-a")
    assert seed_a_revisions.count() == 2

    # Test filtering by seed_slug and revision
    specific_revision = SeedRevision.objects.filter(
        seed_slug="seed-b", revision=3
    ).first()
    assert specific_revision is not None
    assert specific_revision.seed_slug == "seed-b"
    assert specific_revision.revision == 3

    # Test ordering
    latest_revisions = SeedRevision.objects.filter(seed_slug="seed-a").order_by(
        "-revision"
    )

    revisions_list = list(latest_revisions.values_list("revision", flat=True))
    assert revisions_list == [2, 1]


@pytest.mark.django_db
def test_get_latest_revision_for_seed() -> None:
    """Test getting the latest revision for a specific seed."""
    seed_slug = "version-test"

    # Create multiple revisions
    SeedRevision.objects.create(seed_slug=seed_slug, revision=1)
    SeedRevision.objects.create(seed_slug=seed_slug, revision=5)
    SeedRevision.objects.create(seed_slug=seed_slug, revision=3)

    # Get latest revision
    latest = (
        SeedRevision.objects.filter(seed_slug=seed_slug).order_by("-revision").first()
    )

    assert latest.revision == 5


@pytest.mark.django_db
def test_bulk_operations() -> None:
    """Test bulk operations on SeedRevision objects."""
    # Create sample revisions
    SeedRevision.objects.create(seed_slug="sample-1", revision=1)
    SeedRevision.objects.create(seed_slug="sample-1", revision=2)
    SeedRevision.objects.create(seed_slug="sample-2", revision=1)

    # Test bulk update
    SeedRevision.objects.filter(seed_slug="sample-1").update(revision=10)

    updated_revisions = SeedRevision.objects.filter(seed_slug="sample-1")
    for revision in updated_revisions:
        assert revision.revision == 10

    # Test bulk delete
    deleted_count, _ = SeedRevision.objects.filter(seed_slug="sample-1").delete()
    assert deleted_count == 2

    remaining_count = SeedRevision.objects.filter(seed_slug="sample-1").count()
    assert remaining_count == 0
