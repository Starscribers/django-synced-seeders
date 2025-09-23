# Django Synced Seeds Tests

This directory contains comprehensive tests for the django-synced-seeds package using pytest a### Writing New Tests

### Test Organization
- Use function-based tests following pytest conventions
- Use descriptive test names: `test_should_do_something_when_condition`
- Add appropriate markers: `@pytest.mark.django_db`, `@pytest.mark.slow`
- Group related tests in modules, not classesctional test cases.

## Test Structure

The test suite is organized into several modules:

- `test_models.py` - Tests for the SeedRevision model
- `test_seeders.py` - Tests for the Seeder base class, utilities, and registries
- `test_commands.py` - Tests for management commands (syncseeds, exportseed)
- `test_integration.py` - End-to-end integration tests and real-world scenarios
- `conftest.py` - Pytest configuration and shared fixtures
- `settings.py` - Django settings for testing

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-django pytest-cov
```

### Quick Start

Run all tests:
```bash
python run_tests.py
```

Run specific test categories:
```bash
# Unit tests only (fast)
python run_tests.py quick

# Integration tests
python run_tests.py integration

# With coverage reporting
python run_tests.py coverage

# Specific test modules
python run_tests.py models
python run_tests.py commands
python run_tests.py seeders
```

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py

# Run specific test method
pytest tests/test_models.py::TestSeedRevisionModel::test_create_seed_revision

# Run with markers
pytest -m "unit"           # Unit tests only
pytest -m "integration"    # Integration tests only
pytest -m "not slow"       # Skip slow tests

# With coverage
pytest --cov=seeders --cov-report=html

# Debug mode
pytest --pdb -s
```

## Test Categories

### Unit Tests
- **Models**: Test SeedRevision model fields, validation, and database constraints
- **Seeders**: Test Seeder base class, export/import functionality, and registry
- **Utilities**: Test utility functions like `get_seed_meta_path`
- **Commands**: Test management commands with mocking

### Integration Tests
- **Complete Workflows**: End-to-end testing of export → sync cycles
- **Version Management**: Testing incremental updates and revision tracking
- **Multiple Seeders**: Testing coordination between multiple seeders
- **Real-world Scenarios**: Dev-to-staging deployments, hotfix workflows
- **Error Handling**: Permission errors, missing files, invalid data

## Test Features

### Fixtures
- `temp_seed_file` - Temporary JSON seed files
- `temp_meta_file` - Temporary metadata files
- `sample_seed_data` - Predefined test data
- `clean_seed_revisions` - Auto-cleanup of test revisions
- `isolated_registry` - Clean seeder registry for tests

### Database
- Uses in-memory SQLite for speed
- Automatic migrations and cleanup
- Transaction rollback between tests
- `@pytest.mark.django_db` for database access

### Coverage
- Target: 85% code coverage
- HTML reports generated in `htmlcov/`
- Terminal coverage summary
- Coverage of core functionality: models, seeders, commands

## Test Configuration

### pytest.ini
- Django settings: `tests.settings`
- Test discovery patterns
- Coverage configuration
- Custom markers for test organization
- Database optimizations (`--reuse-db`, `--nomigrations`)

### settings.py
- In-memory database for performance
- Minimal Django setup for testing
- Test-specific paths and configurations
- Logging configuration for debugging

## Writing New Tests

### Test Organization
- Group related tests in classes
- Use descriptive test names: `test_should_do_something_when_condition`
- Add appropriate markers: `@pytest.mark.django_db`, `@pytest.mark.slow`

### Best Practices
```python
import pytest

@pytest.mark.django_db
def test_specific_behavior():
    # Arrange
    # Act
    # Assert
    pass

# For database operations requiring transactions
@pytest.mark.django_db(transaction=True)
def test_transaction_behavior():
    pass
```

### Fixtures Usage
```python
def test_with_fixtures(temp_seed_file, sample_seed_data, clean_example_models):
    # Use temporary file
    with temp_seed_file.open('w') as f:
        json.dump(sample_seed_data, f)

    # Test automatically cleans up ExamplePresetModel instances
```

### Mocking External Dependencies
```python
from unittest.mock import patch, Mock

@patch('seeders.seeders.call_command')
def test_load_seed(mock_call_command):
    seeder = Seeder()
    seeder.load_seed()
    mock_call_command.assert_called_once_with("loaddata", seeder.seed_path)
```

## Debugging Tests

### Failed Test Investigation
```bash
# Run last failed tests only
pytest --lf

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Verbose output with full tracebacks
pytest -vvv --tb=long

# Don't capture stdout (see print statements)
pytest -s
```

### Common Issues
1. **Database access**: Add `@pytest.mark.django_db` or use `TestCase`
2. **File permissions**: Tests create temporary files that may need cleanup
3. **Registry pollution**: Use `isolated_registry` fixture for seeder tests
4. **Path issues**: Tests use temporary directories, check path handling

## Performance

- **Fast unit tests**: < 1 second per test
- **Integration tests**: 2-10 seconds per test
- **Full suite**: < 30 seconds
- **Database**: In-memory SQLite for speed
- **Parallel execution**: Can be enabled with `pytest-xdist`

## Continuous Integration

The test suite is designed to run in CI environments:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    python run_tests.py coverage

- name: Upload coverage
  uses: codecov/codecov-action@v1
```

## Test Data

Tests use the `playground` app with `ExamplePresetModel` for realistic scenarios:
- Simple model with name and value fields
- Registered seeder for end-to-end testing
- Temporary data that's cleaned up automatically

## Maintenance

### Adding New Tests
1. Choose appropriate test module based on functionality
2. Create function-based tests following pytest conventions
3. Use existing fixtures where possible
4. Add new fixtures to `conftest.py` if needed
5. Update markers in `pytest.ini` if introducing new test categories

### Updating Coverage Requirements
Adjust coverage requirements in:
- `pytest.ini`: `--cov-fail-under=85`
- `run_tests.py`: coverage test function

### Performance Tuning
- Use `--reuse-db` to avoid recreating test database
- Use `--nomigrations` to speed up database setup
- Profile slow tests and optimize or mark as `@pytest.mark.slow`
