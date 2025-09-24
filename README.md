# Django Synced Seeds

[![PyPI version](https://badge.fury.io/py/django-synced-seeders.svg)](https://badge.fury.io/py/django-synced-seeders)
[![Python Support](https://img.shields.io/pypi/pyversions/django-synced-seeders.svg)](https://pypi.org/project/django-synced-seeders/)
[![Django Support](https://img.shields.io/badge/Django-4.2%2B-brightgreen.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Starscribers/python-packages/actions/workflows/test.yml/badge.svg)](https://github.com/Starscribers/python-packages/actions)

An easy-to-use seeder manager to keep seed data in sync across multiple environments. Perfect for managing reference data, initial configurations, and test data across development, staging, and production environments.

## Features

✨ **Version Control for Seeds** - Track and manage seed versions with automatic revision tracking
🔄 **Environment Sync** - Keep data consistent across development, staging, and production
📦 **Export & Import** - Easy data export from any environment and import to others
🎯 **Selective Loading** - Load only the seeds you need with intelligent version checking
🏗️ **Django Integration** - Built specifically for Django with full ORM support
🧪 **Test-Friendly** - Comprehensive test suite with function-based tests
🔧 **Extensible** - Easy to extend with custom seeders for your specific needs

## Quick Start

### Installation

```bash
pip install django-synced-seeders
```

### Add to Django Settings

```python
# settings.py
INSTALLED_APPS = [
    # ... your apps
    'seeders',
]

# Optional: Custom seed metadata path
SEEDS_META_PATH = BASE_DIR / "seeds_meta.json"
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Your First Seeder

```python
# myapp/seeders.py
from seeds.registries import seeder_registry
from seeds.seeders import Seeder
from .models import Category, Tag

@seeder_registry.register()
class CategorySeeder(Seeder):
    """Seeder for category reference data."""

    seed_slug = "categories"
    exporting_querysets = (Category.objects.all(),)

    # Optional: whether to delete existing data before loading
    delete_existing = True

@seeder_registry.register()
class TagSeeder(Seeder):
    """Seeder for tag data."""

    seed_slug = "tags"
    exporting_querysets = (Tag.objects.all(),)
```

### Export Data

```bash
# Export data from current environment
python manage.py exportseed categories
python manage.py exportseed tags
```

### Sync Data to Another Environment

```bash
# Import all available seeds
python manage.py syncseeds
```

## Core Concepts

### Seeders

A **Seeder** is a Python class that defines how to export and import specific data. Each seeder:

- Has a unique `seed_slug` identifier
- Defines which data to export via `exporting_querysets`
- Manages the seed file path and format
- Controls whether to delete existing data before importing

### Version Management

Seeds are automatically versioned using a metadata file (`seeds_meta.json`). Each time you export:

1. The revision number increments
2. Only newer versions are imported during sync
3. Already up-to-date seeds are skipped

### Registry System

Seeders are automatically discovered and registered using the `@seeder_registry.register()` decorator. The registry:

- Auto-discovers seeders in `*/seeders.py` files
- Provides access to all registered seeders
- Enables the management commands to find your seeders

## Usage Examples

### Development Workflow

```bash
# 1. Create some reference data in your dev environment
# (through admin, fixtures, or manual creation)

# 2. Export the data
python manage.py exportseed categories
python manage.py exportseed user_roles

# 3. Commit the generated seed files and metadata
git add seeds/ seeds_meta.json
git commit -m "Add category and user role seeds"

# 4. Deploy to staging/production
git pull
python manage.py syncseeds
```

### Custom Seeder with Filtering

```python
from seeds.registries import seeder_registry
from seeds.seeders import Seeder
from myapp.models import User, UserProfile

@seeder_registry.register()
class AdminUserSeeder(Seeder):
    """Seeder for admin users only."""

    seed_slug = "admin_users"

    # Custom queryset filtering
    exporting_querysets = (
        User.objects.filter(is_superuser=True),
        UserProfile.objects.filter(user__is_superuser=True),
    )

    # Don't delete existing admins
    delete_existing = False
```

### Environment-Specific Seeds

```python
from django.conf import settings
from seeds.registries import seeder_registry
from seeds.seeders import Seeder

@seeder_registry.register()
class ConfigSeeder(Seeder):
    """Environment-specific configuration seeder."""

    seed_slug = "app_config"

    def __init__(self):
        super().__init__()

        # Different seed file per environment
        env = getattr(settings, 'ENVIRONMENT', 'dev')
        self.seed_path = f"seeds/config_{env}.json"

    @property
    def exporting_querysets(self):
        from myapp.models import AppConfig
        return (AppConfig.objects.filter(environment=settings.ENVIRONMENT),)
```

### Complex Data Relationships

```python
@seeder_registry.register()
class BlogSeeder(Seeder):
    """Seeder for blog content with relationships."""

    seed_slug = "blog_content"

    exporting_querysets = (
        # Export in dependency order
        Category.objects.all(),
        Tag.objects.all(),
        Author.objects.all(),
        Post.objects.all(),
        PostTag.objects.all(),  # Many-to-many through table
    )

    def get_export_objects(self):
        """Custom export logic with proper ordering."""
        from itertools import chain

        # Ensure categories and tags are first
        categories = Category.objects.all()
        tags = Tag.objects.all()
        authors = Author.objects.filter(posts__isnull=False).distinct()
        posts = Post.objects.select_related('category', 'author')
        post_tags = PostTag.objects.select_related('post', 'tag')

        return chain(categories, tags, authors, posts, post_tags)
```

## Management Commands

### exportseed

Export data for a specific seeder:

```bash
python manage.py exportseed <seed_slug>

# Examples
python manage.py exportseed categories
python manage.py exportseed user_permissions
```

**What it does:**
1. Finds the seeder by slug
2. Exports data using the seeder's `exporting_querysets`
3. Saves data to JSON file
4. Increments version number in metadata file

### syncseeds

Import all available seeds that need updating:

```bash
python manage.py syncseeds
```

**What it does:**
1. Discovers all registered seeders
2. Compares local vs. available versions
3. Imports only newer versions
4. Skips already up-to-date seeds
5. Creates revision records for tracking

**Example Output:**
```
[Synced Seeders] Syncing seeds...
[Synced Seeders] Fixture categories is installed (Not installed -> v3).
[Synced Seeders] Fixture tags is already synced, skipped.
[Synced Seeders] Fixture user_roles is installed (v1 -> v2).
[Synced Seeders] Synced 2 seeds.
```

## File Structure

After using django-synced-seeds, your project structure will look like:

```
your_project/
├── seeds/                          # Seed data files
│   ├── categories.json
│   ├── tags.json
│   └── user_roles.json
├── seeds_meta.json                 # Version metadata
├── myapp/
│   ├── seeders.py                  # Your seeder definitions
│   └── models.py
└── manage.py
```

### seeds_meta.json Example

```json
{
    "categories": 3,
    "tags": 1,
    "user_roles": 2
}
```

### Seed File Example

```json
[
    {
        "model": "myapp.category",
        "pk": 1,
        "fields": {
            "name": "Technology",
            "slug": "technology",
            "description": "Tech-related content"
        }
    },
    {
        "model": "myapp.category",
        "pk": 2,
        "fields": {
            "name": "Business",
            "slug": "business",
            "description": "Business and finance content"
        }
    }
]
```

## Advanced Configuration

### Custom Seed Paths

```python
# settings.py
SEEDS_META_PATH = BASE_DIR / "custom_seeds" / "metadata.json"
```

```python
# Custom seeder with specific path
class CustomSeeder(Seeder):
    seed_slug = "custom_data"
    seed_path = "custom_seeds/my_data.json"
    exporting_querysets = (MyModel.objects.all(),)
```

### Conditional Seeding

```python
class ConditionalSeeder(Seeder):
    seed_slug = "conditional_data"

    def load_seed(self):
        """Override to add custom logic."""
        if settings.DEBUG:
            # Only load in development
            super().load_seed()
        else:
            self.stdout.write("Skipping conditional seed in production")

    @property
    def exporting_querysets(self):
        # Dynamic querysets based on environment
        if settings.DEBUG:
            return (TestData.objects.all(),)
        return (ProductionData.objects.all(),)
```

### Integration with Django Fixtures

Django Synced Seeds works alongside Django's built-in fixtures:

```python
# You can still use regular fixtures
python manage.py loaddata initial_data.json

# And use synced seeds for environment-specific data
python manage.py syncseeds
```

## Testing

Django Synced Seeds includes a comprehensive test suite with function-based tests:

```bash
# Install test dependencies
pip install django-synced-seeders[testing]

# Run all tests
python -m pytest

# Run specific test categories
python -m pytest -m "not slow"  # Skip slow tests
python -m pytest tests/test_models.py  # Just model tests
python -m pytest tests/test_integration.py  # Integration tests

# With coverage
python -m pytest --cov=seeders --cov-report=html
```

### Writing Tests for Your Seeders

```python
import pytest
from django.test import override_settings
from myapp.models import Category
from myapp.seeders import CategorySeeder

@pytest.mark.django_db
def test_category_seeder_export():
    """Test exporting category data."""
    # Create test data
    Category.objects.create(name="Test Category", slug="test")

    seeder = CategorySeeder()
    seeder.seed_path = "/tmp/test_categories.json"

    # Test export
    seeder.export()

    # Verify file was created
    assert Path(seeder.seed_path).exists()

@pytest.mark.django_db
def test_category_seeder_load():
    """Test loading category data."""
    seeder = CategorySeeder()
    seeder.seed_path = "fixtures/test_categories.json"

    # Load seed data
    seeder.load_seed()

    # Verify data was imported
    assert Category.objects.filter(name="Test Category").exists()
```

## Best Practices

### 1. **Organize Seeders by Domain**

```python
# users/seeders.py - User-related seeds
class UserRoleSeeder(Seeder): ...
class PermissionSeeder(Seeder): ...

# content/seeders.py - Content-related seeds
class CategorySeeder(Seeder): ...
class TagSeeder(Seeder): ...
```

### 2. **Use Descriptive Seed Slugs**

```python
# Good
seed_slug = "user_permissions"
seed_slug = "blog_categories"
seed_slug = "payment_providers"

# Avoid
seed_slug = "data"
seed_slug = "stuff"
seed_slug = "seed1"
```

### 3. **Order Dependencies Properly**

```python
class BlogSeeder(Seeder):
    # Export dependencies first
    exporting_querysets = (
        Author.objects.all(),      # No dependencies
        Category.objects.all(),    # No dependencies
        Post.objects.all(),        # Depends on Author, Category
        Comment.objects.all(),     # Depends on Post
    )
```

### 4. **Handle Sensitive Data**

```python
class UserSeeder(Seeder):
    """Seeder that excludes sensitive data."""

    @property
    def exporting_querysets(self):
        # Exclude sensitive fields or users
        return (
            User.objects.exclude(is_superuser=True)
                        .only('username', 'email', 'first_name', 'last_name'),
        )
```

### 5. **Environment-Specific Configuration**

```python
# settings/development.py
SEEDS_META_PATH = BASE_DIR / "seeds" / "dev_meta.json"

# settings/production.py
SEEDS_META_PATH = BASE_DIR / "seeds" / "prod_meta.json"
```

### 6. **Version Control Best Practices**

```bash
# Always commit seeds and metadata together
git add seeds/ seeds_meta.json
git commit -m "Update user role seeds to v3"

# Use .gitignore for environment-specific seeds if needed
echo "seeds/local_*.json" >> .gitignore
```

### 7. **Deployment Integration**

```bash
# In your deployment script
python manage.py migrate        # Run migrations first
python manage.py syncseeds      # Then sync seed data
python manage.py collectstatic  # Then static files
```

## Troubleshooting

### Common Issues

**Q: Seeds aren't being discovered**
```python
# Make sure your seeders.py file is in the right location
myapp/
├── seeders.py  # ✓ Will be discovered
└── models.py

# And uses the registry decorator
@seeder_registry.register()
class MySeeder(Seeder): ...
```

**Q: "Seed path is not set" error**
```python
# Either set seed_path explicitly
class MySeeder(Seeder):
    seed_path = "seeds/my_data.json"

# Or let it use the default (seeds/{seed_slug}.json)
class MySeeder(Seeder):
    seed_slug = "my_data"  # Will use seeds/my_data.json
```

**Q: Data not loading correctly**
```python
# Check your exporting_querysets
class MySeeder(Seeder):
    exporting_querysets = (
        MyModel.objects.all(),  # Make sure this returns data
    )

    # Debug what's being exported
    def get_export_objects(self):
        objects = super().get_export_objects()
        print(f"Exporting {len(list(objects))} objects")
        return super().get_export_objects()
```

**Q: Version conflicts**
```bash
# Check current versions
cat seeds_meta.json

# Force re-export if needed
python manage.py exportseed my_seeder

# Or manually edit seeds_meta.json to reset versions
```

### Debug Mode

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'seeders': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## API Reference

### Seeder Class

```python
class Seeder:
    """Base seeder class."""

    # Configuration attributes
    seed_slug: str = "base-seed"
    seed_path: str | None = None
    delete_existing: bool = True
    exporting_querysets: tuple = ()

    # Methods
    def __init__(self) -> None: ...
    def load_seed(self) -> None: ...
    def export(self) -> None: ...
    def get_export_objects(self) -> Iterable: ...
```

### Registry Functions

```python
from seeds.registries import seeder_registry

# Register a seeder
@seeder_registry.register()
class MySeeder(Seeder): ...

# Access registered seeders
all_seeders = seeder_registry.registry
my_seeder_class = seeder_registry.registry["my_slug"]
```

### Utility Functions

```python
from seeds.utils import get_seed_meta_path

# Get metadata file path
meta_path = get_seed_meta_path()
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Starscribers/python-packages.git
cd python-packages/django-synced-seeds

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e .[dev,testing]

# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=seeders --cov-report=html

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/
```
**Happy coding!** 🎉
Join our discord open source community: https://discord.gg/ngE8JxjDx7