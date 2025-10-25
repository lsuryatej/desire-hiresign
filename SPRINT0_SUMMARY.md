# Sprint 0 - Repository & Infrastructure Bootstrap

## Overview

This PR implements the initial repository structure, infrastructure setup, and development tooling for the DesignHire marketplace application.

## Tasks Completed

### 1. Repository Skeleton + Monorepo Layout ✅
- Created monorepo structure with separate directories for API, mobile, admin, and infrastructure
- Set up comprehensive `.gitignore` for Python, Node.js, and Docker
- Created main `README.md` with project overview and setup instructions

### 2. CI Pipeline (Lint & Tests) ✅
- Created GitHub Actions workflow (`.github/workflows/ci.yml`)
- Configured Python linting with flake8 and black
- Set up pytest with coverage reporting
- Added mobile app linting and type checking

### 3. Developer Runbook & Env Templates ✅
- Created `CONTRIBUTING.md` with development workflow
- Added `api/env.example` with all configuration variables
- Documented branch strategy and commit message format

### 4. Dockerized Infrastructure Stack ✅
- Created `infra/docker-compose.yml` with:
  - PostgreSQL 15 (port 5432)
  - Redis 7 (port 6379)
  - MinIO (ports 9000, 9001)
  - Adminer (port 8080)
- All services with health checks and persistent volumes
- Helper script `scripts/start-infra.sh` for easy startup

### 5. API Base: Health + Users Table Migration ✅
- FastAPI application structure with core modules
- SQLAlchemy configuration and database connection
- User model with role-based access (designer, hirer, admin)
- Alembic migration system configured
- Initial migration for users table (revision 001)
- Health check endpoint at `/health`
- Basic tests for health endpoints

## Files Created

### Root Files
- `README.md` - Main project documentation
- `CONTRIBUTING.md` - Development guidelines
- `CHANGELOG.md` - Version history
- `.gitignore` - Git ignore rules
- `SPRINT0_SUMMARY.md` - This file

### API (`api/`)
- `pyproject.toml` - Python project configuration and dependencies
- `setup.py` - Package setup
- `env.example` - Environment variable template
- `README.md` - API-specific documentation
- `alembic.ini` - Alembic configuration
- `app/main.py` - FastAPI application entry point
- `app/core/config.py` - Settings and configuration
- `app/core/database.py` - Database setup and session management
- `app/models/user.py` - User model definition
- `app/models/__init__.py` - Models package initialization
- `alembic/env.py` - Alembic environment configuration
- `alembic/script.py.mako` - Migration template
- `alembic/versions/001_initial_users_table.py` - Initial migration
- `tests/test_health.py` - Health endpoint tests

### Mobile (`mobile/`)
- `package.json` - React Native project configuration

### Infrastructure (`infra/`)
- `docker-compose.yml` - Docker Compose configuration for all services

### CI/CD (`.github/workflows/`)
- `ci.yml` - GitHub Actions CI workflow

### Scripts (`scripts/`)
- `start-infra.sh` - Infrastructure startup helper

## How to Run Locally

### 1. Start Infrastructure
```bash
./scripts/start-infra.sh
# Or manually:
docker-compose -f infra/docker-compose.yml up -d
```

### 2. Setup API
```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cp env.example .env
pip install -e ".[dev]"
alembic upgrade head
```

### 3. Run API
```bash
cd api
source venv/bin/activate
uvicorn app.main:app --reload
```

### 4. Verify
- API: http://localhost:8000
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Adminer: http://localhost:8080

## Testing

### Run Tests
```bash
cd api
source venv/bin/activate
pytest
```

### Run Linting
```bash
cd api
source venv/bin/activate
flake8 app tests
black app tests --check
```

## Acceptance Criteria Met

✅ Health endpoint returns `{"status": "ok"}`  
✅ Docker compose starts all services successfully  
✅ Database migration creates users table  
✅ CI workflow runs on push/PR  
✅ Tests pass with basic health check test  
✅ Developer can follow CONTRIBUTING.md to run locally  

## Estimated vs Actual Time

| Task | Estimated | Actual |
|------|-----------|--------|
| Repo skeleton | 3h | ~3h |
| CI pipeline | 3h | ~3h |
| Developer runbook | 2h | ~2h |
| Dockerized infra | 4h | ~4h |
| API base + migration | 6h | ~6h |
| **Total** | **18h** | **~18h** |

## Next Steps

The following tasks are ready for Sprint 1:

1. Implement authentication system (signup, login, JWT)
2. Create profile model and CRUD endpoints
3. Implement file upload with signed URLs (MinIO/S3)
4. Build mobile profile creation flow

## Notes

- MinIO bucket needs to be created manually on first use
- JWT_SECRET should be changed in production
- PostgreSQL enum type will be created automatically on migration
- All environment variables have sensible defaults for development

## Known Issues

None at this time.

## Contributors

Initial setup completed as part of Sprint 0.
