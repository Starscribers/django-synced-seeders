# Contributing to Any Registries

Thank you for considering contributing to Any Registries! This document outlines the process for contributing to this project.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- uv (recommended) or pip for package management
- Git

### Setting up the development environment

1. Clone the repository:
```bash
git clone https://github.com/Starscribers/python-packages.git
cd python-packages/any-registries
```

2. Install dependencies:
```bash
uv sync --dev
```

3. Install pre-commit hooks:
```bash
uv run pre-commit install
```

4. Run tests to ensure everything is working:
```bash
uv run pytest
```

## Development Workflow

### Before making changes

1. Create a new branch from `main`:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

2. Make sure pre-commit hooks are installed:
```bash
uv run pre-commit install
```

### Making changes

1. Write your code following the existing style
2. Add or update tests as needed
3. Update documentation if necessary
4. Run the development checks:

```bash
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type check
uv run mypy src/

# Run tests
uv run pytest

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

### Submitting changes

1. Commit your changes:
```bash
git add .
git commit -m "feat: add your feature description"
# or
git commit -m "fix: fix your bug description"
```

2. Push your branch:
```bash
git push origin feature/your-feature-name
```

3. Create a Pull Request on GitHub

## Code Style

This project uses:
- **ruff** for linting and formatting
- **mypy** for type checking
- **bandit** for security analysis
- **pre-commit** for automated checks

All code must pass these checks before being merged.

### Commit Message Format

We follow the conventional commits specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test-related changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=any_registries

# Run specific test file
uv run pytest tests/test_registry.py

```

### Writing Tests

- Write tests for all new functionality
- Ensure tests are isolated and deterministic
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases

### Test Structure

Tests are organized as follows:
- `tests/test_registry.py` - Core registry functionality tests

## Documentation

### Updating Documentation

- Update the README.md for user-facing changes
- Add docstrings to new functions and classes
- Update type hints
- Include usage examples for new features

### Documentation Style

- Use Google-style docstrings
- Include type hints for all function parameters and return values
- Provide usage examples where appropriate

## Pull Request Guidelines

### Before submitting

- [ ] All tests pass
- [ ] Code is properly formatted and linted
- [ ] Type checking passes
- [ ] Security checks pass
- [ ] Documentation is updated
- [ ] Commit messages follow the conventional format

### Pull Request Template

When creating a pull request, include:

1. **Description**: What does this PR do?
2. **Type of change**: Bug fix, new feature, documentation, etc.
3. **Testing**: How has this been tested?
4. **Checklist**: Confirm all requirements are met

## Release Process

Releases are automated through GitHub Actions:

1. Create a new release on GitHub
2. GitHub Actions will automatically:
   - Run all tests
   - Build the package
   - Publish to PyPI (for maintainers)

## Getting Help

If you need help or have questions:

1. Check existing issues on GitHub
2. Create a new issue with the "question" label
3. Provide detailed information about your problem or question

## Code of Conduct

Please be respectful and inclusive in all interactions. We want this to be a welcoming environment for all contributors.

Thank you for contributing! 🎉
