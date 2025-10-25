# Contributing to DesignHire

Thank you for your interest in contributing to DesignHire! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd deshire-hiresign
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose -f infra/docker-compose.yml up -d
   ```

3. **Setup API**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cp env.example .env
   pip install -e ".[dev]"
   alembic upgrade head
   ```

4. **Setup Mobile App**
   ```bash
   cd mobile
   npm install
   ```

5. **Run API**
   ```bash
   cd api
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

6. **Run Mobile App**
   ```bash
   cd mobile
   npm start
   # In another terminal
   npm run ios  # or npm run android
   ```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `task/description` - Feature branches

### Creating a New Feature

1. **Create a feature branch**
   ```bash
   git checkout -b task/add-user-authentication
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Write tests for new functionality
   - Update documentation as needed

3. **Run tests and linting**
   ```bash
   # API
   cd api
   pytest
   flake8 app tests
   black app tests --check
   
   # Mobile
   cd mobile
   npm run lint
   npm run test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "[TASK] Add user authentication - Description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin task/add-user-authentication
   ```

### Commit Message Format

```
[TASK] Brief title

Detailed description of what and why. Include any breaking changes.

Fixes #123
```

Prefixes:
- `[TASK]` - New feature or task implementation
- `[FIX]` - Bug fix
- `[DOC]` - Documentation changes
- `[REFACTOR]` - Code refactoring
- `[TEST]` - Test additions or changes

## Code Style

### Python (API)

- Use Black for formatting (line length: 100)
- Follow PEP 8 conventions
- Use type hints where appropriate
- Write docstrings for public functions/classes

```python
def calculate_score(
    user: User,
    target: Profile,
    weights: Dict[str, float]
) -> float:
    """Calculate matching score between user and target profile.
    
    Args:
        user: The user profile
        target: The target profile
        weights: Scoring weights for different factors
        
    Returns:
        Matching score between 0 and 1
    """
    pass
```

### TypeScript/React Native (Mobile)

- Use TypeScript strict mode
- Follow React Native best practices
- Use functional components with hooks
- Use ESLint and Prettier

```typescript
interface ProfileCardProps {
  profile: Profile;
  onSwipe: (direction: SwipeDirection) => void;
}

export const ProfileCard: React.FC<ProfileCardProps> = ({
  profile,
  onSwipe,
}) => {
  // Component implementation
};
```

## Testing

### API Tests

```bash
cd api
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_auth.py::test_login_success
```

### Mobile Tests

```bash
cd mobile
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```

## Pull Request Process

1. **Update documentation** - README, API docs, etc.
2. **Add tests** - Ensure tests pass
3. **Update CHANGELOG** - Document changes
4. **Create PR** - Fill out PR template
5. **Address review feedback** - Respond to comments
6. **Get approval** - Wait for review
7. **Merge** - Squash and merge when approved

### PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Changes Made
- Feature 1
- Fix 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for new functionality
- [ ] All tests pass locally
```

## Database Migrations

When modifying models:

```bash
cd api
# Create migration
alembic revision --autogenerate -m "Add user profile table"

# Review migration file
# Edit if needed

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## Getting Help

- Create an issue for bugs or feature requests
- Ask questions in discussions
- Check existing issues before creating new ones

## Code of Conduct

Be respectful, inclusive, and professional in all interactions. Harassment of any kind is not tolerated.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
