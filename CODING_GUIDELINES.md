## General Guidelines
- Leave blank lines to separate logic sections
- Prevent abbreviating non-common or non-proper words
- Method names should always be verbs or is_

## Tests
- Always use pytest for testing


## Commit Messages- Use the imperative mood in the subject line
- Limit the subject line to 50 characters
- Capitalize the subject line
- Do not end the subject line with a period
- Use the body to explain what and why vs. how
example:
```
feat: add new registry support
```

## Branch Naming
- Use `feature/` prefix for new features
- Use `fix/` prefix for bug fixes
- Use `docs/` prefix for documentation changes
- Use `test/` prefix for test-related changes
- Use `refactor/` prefix for code refactoring
- Use `chore/` prefix for maintenance tasks

## Pull Requests
- Include tests for new features or bug fixes
- Ensure all tests pass before creating a PR
- Link related issues in the PR description
- Request reviews from at least one team member
- Use descriptive titles and detailed descriptions
- Squash commits when merging to keep history clean
- Delete the branch after merging
- Follow the conventional commits specification for commit messages
- Ensure code adheres to the project's coding standards and passes all linting checks
- Ensure PRs are small and focused on a single task or issue
