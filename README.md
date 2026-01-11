# Django Synced Seeds

[![PyPI version](https://badge.fury.io/py/django-synced-seeders.svg)](https://badge.fury.io/py/django-synced-seeders)
[![Python Support](https://img.shields.io/pypi/pyversions/django-synced-seeders.svg)](https://pypi.org/project/django-synced-seeders/)
[![Django Support](https://img.shields.io/badge/Django-4.2%2B-brightgreen.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An easy-to-use seeder manager to keep seed data in sync across multiple environments. Perfect for managing reference data, initial configurations, and test data across development, staging, and production environments.

## Installation

```bash
pip install django-synced-seeders
```

Add to your Django settings:

```python
# settings.py
INSTALLED_APPS = [
    # ... your apps
    'seeds',
]
```

Run migrations:

```bash
python manage.py migrate
```

## Quick Start

1. Create your first seeder:

```python
# myapp/seeders.py
from seeds import seeder_registry, Seeder
from .models import Category

@seeder_registry.register()
class CategorySeeder(Seeder):
    seed_slug = "categories"
    priority = 10  # Lower numbers load first (default: 100)
    exporting_querysets = (Category.objects.all(),)
```

2. Export data:

```bash
python manage.py exportseed categories
```

3. Sync to another environment:

```bash
python manage.py syncseeds
```

## Tagging Seeders

Organize seeders with tags for targeted execution:

```python
# myapp/seeders.py
from seeds import seeder_registry, Seeder
from .models import User, Product

@seeder_registry.register(tags="e2e")
class E2ETestSeeder(Seeder):
    seed_slug = "e2e_test_data"
    exporting_querysets = (User.objects.all(),)

@seeder_registry.register(tags=["development", "demo"])
class DemoSeeder(Seeder):
    seed_slug = "demo_data"
    exporting_querysets = (Product.objects.all(),)
```

Run seeders by tag:

```bash
# Sync only e2e tagged seeders
python manage.py syncseeds e2e

# Sync multiple tags (union of all matching seeders)
python manage.py syncseeds e2e development

# Sync all seeders (default behavior)
python manage.py syncseeds
```

## Documentation

📚 **Full Documentation**: [https://starscribers.github.io/django-synced-seeders/](https://starscribers.github.io/django-synced-seeders/)

## Community & Support

💬 **Discord Server**: [Join our community](https://discord.gg/ngE8JxjDx7) for discussions, support, and updates.

## License

This project is licensed under the MIT License.
