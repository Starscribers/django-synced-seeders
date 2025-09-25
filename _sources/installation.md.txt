# Installation

## Requirements

- Python 3.9+
- Django 4.2+
- Any database supported by Django

## Install from PyPI

### Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that can significantly speed up installations:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv

# Install django-synced-seeders
uv add django-synced-seeders
```

### Using pip

```bash
pip install django-synced-seeders
```

## Add to Django Settings

Add `seeders` to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    # ... your other apps
    'seeders',
]

# Optional: Custom seed metadata path
SEEDS_META_PATH = BASE_DIR / "seeds_meta.json"
```

## Run Migrations

Run Django migrations to create the necessary database tables:

```bash
python manage.py migrate
```

## Development Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/Starscribers/django-synced-seeders.git
cd django-synced-seeders/django-synced-seeders

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync --group dev --group testing --group docs

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/Starscribers/django-synced-seeders.git
cd django-synced-seeders/django-synced-seeders

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e .[dev,testing,docs]
```

## Next Steps

Once installed, you can:

1. [Create your first seeder](usage.md#create-your-first-seeder)
2. [Learn about core concepts](concepts.md)
3. [Explore usage examples](examples.md)
