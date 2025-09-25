# Contributing

We welcome contributions! Please follow these guidelines to contribute to django-synced-seeders.

## Development Setup

### 1. Clone and Setup

#### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/Starscribers/django-synced-seeders.git
cd django-synced-seeders/django-synced-seeders

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv

# Create virtual environment and install all dependencies
uv sync --group dev --group testing --group docs

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Using pip

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

### 2. Run Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=seeders --cov-report=html

# Run specific test categories
python -m pytest -m "not slow"  # Skip slow tests
python -m pytest tests/test_models.py  # Just model tests
```

### 3. Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/
```

### 4. Build Documentation

#### Using uv (Recommended)

```bash
# Build documentation with uv
./scripts/build-docs.sh

# Or manually:
uv sync --group docs
cd docs/
uv run sphinx-build -b html . _build/html
```

#### Using pip

```bash
# Install docs dependencies
pip install -e .[docs]

# Build documentation
cd docs/
make html
# or
sphinx-build -b html . _build/html
```

## Contribution Process

### 1. Create an Issue

Before starting work, please create an issue describing:
- What you want to add/change
- Why it's needed
- How you plan to implement it

### 2. Fork and Branch

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/yourusername/django-synced-seeders.git
cd django-synced-seeders/django-synced-seeders

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write code following the existing style
- Add tests for new functionality
- Update documentation if needed
- Ensure all tests pass

### 4. Submit Pull Request

- Push your branch to your fork
- Create a pull request with a clear description
- Reference any related issues
- Wait for review and address feedback

## Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints for all public APIs
- Write docstrings for classes and functions
- Keep functions small and focused

```python
def export_seed(self, seeder_slug: str) -> None:
    """Export seed data for the given seeder.
    
    Args:
        seeder_slug: The slug of the seeder to export
        
    Raises:
        SeederNotFound: If the seeder doesn't exist
    """
    # Implementation here
```

### Testing

- Write function-based tests using pytest
- Test both success and failure cases
- Use descriptive test names
- Mock external dependencies

```python
@pytest.mark.django_db
def test_seeder_export_creates_file():
    """Test that exporting creates a seed file."""
    # Test implementation
```

### Documentation

- Update relevant documentation files
- Add examples for new features
- Keep API documentation current
- Write clear, concise explanations

## Project Structure

```
django-synced-seeders/
├── src/
│   ├── seeds/              # Main package
│   │   ├── models.py       # Django models
│   │   ├── seeders.py      # Seeder base class
│   │   ├── registries.py   # Registry system
│   │   ├── utils.py        # Utility functions
│   │   └── management/     # Management commands
│   └── playground/         # Test Django project
├── tests/                  # Test suite
├── docs/                   # Documentation
└── pyproject.toml         # Package configuration
```

## Testing Guidelines

### Test Categories

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **Functional tests**: Test end-to-end workflows

### Test Database

Tests use an in-memory SQLite database for speed. For database-specific features, add additional test configurations.

### Fixtures and Factories

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def sample_seeder():
    """Create a sample seeder for testing."""
    return SampleSeeder()

@pytest.fixture
def temp_seed_file():
    """Create a temporary seed file."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        yield f.name
    os.unlink(f.name)
```

## Documentation Guidelines

### Structure

- Keep documentation focused and scannable
- Use clear headings and sections
- Include practical examples
- Link between related topics

### Writing Style

- Use active voice
- Write for different skill levels
- Include code examples
- Explain the "why" not just the "how"

### API Documentation

- Document all public classes and methods
- Include parameter types and descriptions
- Show example usage
- Note any side effects or exceptions

## Release Process

### Version Numbers

We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create git tag: `git tag v1.2.3`
5. Push tag: `git push origin v1.2.3`
6. GitHub Actions will build and publish to PyPI

## Community

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions
- **Discord**: Community chat and questions
- **Discussions**: Long-form discussions and ideas

### Code of Conduct

We follow a simple code of conduct:
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume positive intent

### Recognition

Contributors are recognized in:
- GitHub contributor list
- Release notes for significant contributions
- Special thanks for major features

## Common Tasks

### Adding a New Feature

1. Create an issue describing the feature
2. Write tests for the expected behavior
3. Implement the feature
4. Update documentation
5. Submit pull request

### Fixing a Bug

1. Create a test that reproduces the bug
2. Fix the bug
3. Ensure the test passes
4. Submit pull request

### Updating Documentation

1. Identify what needs updating
2. Make changes in relevant docs/ files
3. Test any code examples
4. Submit pull request

## Getting Help

Need help contributing?

- **Join our Discord**: https://discord.gg/ngE8JxjDx7
- **Read existing issues**: See what others are working on
- **Start small**: Look for "good first issue" labels
- **Ask questions**: We're happy to help new contributors

Thank you for contributing to django-synced-seeders! 🎉