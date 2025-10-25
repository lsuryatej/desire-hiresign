# DesignHire - Tinder-Style Designer Marketplace

A two-sided marketplace connecting designers with hirers through a swipe-to-discover interface and job listing platform.

## Architecture

- **Mobile App**: React Native (iOS & Android)
- **Backend API**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache/Queue**: Redis + RQ
- **Media Storage**: MinIO (S3-compatible)
- **Admin Panel**: React (web)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for mobile app)
- Python 3.11+ (for API)

### 1. Start Infrastructure

```bash
docker-compose -f infra/docker-compose.yml up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (port 9000, UI: 9001)
- Adminer (port 8080)

### 2. Setup API

```bash
cd api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
alembic upgrade head
python scripts/seed.py  # Optional: add demo data
uvicorn app.main:app --reload
```

API runs on http://localhost:8000
- Docs: http://localhost:8000/docs

### 3. Setup Mobile App

```bash
cd mobile
npm install
npm run ios  # or npm run android
```

### 4. Access Services

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Adminer: http://localhost:8080 (user: postgres, pass: password, db: app)
- MinIO Console: http://localhost:9001 (user: minio, pass: minio123)

## Environment Variables

Copy `.env.example` to `.env` in each service and configure:

```bash
# API (.env)
POSTGRES_URL=postgresql://postgres:password@localhost:5432/app
REDIS_URL=redis://localhost:6379/0
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minio
MINIO_SECRET_KEY=minio123
JWT_SECRET=your-secret-key-here-change-in-production
```

## Development Workflow

1. Create feature branch: `git checkout -b task/describe-feature`
2. Make changes and test locally
3. Write/update tests
4. Run tests: `cd api && pytest`
5. Commit with clear message: `[TASK] Title - Description`
6. Push and create PR
7. Run E2E tests before merging

## Testing

```bash
# API unit tests
cd api && pytest

# E2E tests (when implemented)
npm run test:e2e

# Linting
cd api && flake8 app tests
cd mobile && npm run lint
```

## Project Structure

```
/
├── api/                # FastAPI backend
│   ├── app/
│   ├── alembic/       # Database migrations
│   └── tests/         # Test suite
├── mobile/            # React Native app
│   ├── src/
│   │   ├── design/    # Design system tokens
│   │   └── screens/
│   └── __tests__/
├── admin/             # Admin web panel
├── infra/             # Docker compose & infra configs
├── scripts/           # Seed data & utilities
└── .github/           # CI/CD workflows
```

## Design System

We follow a minimalist, low-strain design system across all platforms:

- **Colors**: Muted, calm palette (#F6F7F9 background, #3B82F6 primary)
- **Typography**: Inter font, 14-28px scale
- **Spacing**: 8px base unit (8, 16, 24, 32px)
- **Components**: Cards, forms, chat with consistent styling

See [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) for full specifications.

## Sprint Progress

- [x] Sprint 0: Repo setup & infrastructure
- [ ] Sprint 1: Auth & Profiles
- [ ] Sprint 2: Listings & Media
- [ ] Sprint 3: Swipe Feed & Interactions
- [ ] Sprint 4: Matches & Messaging
- [ ] Sprint 5: Admin & Moderation
- [ ] Sprint 6: Search & Onboarding
- [ ] Sprint 7: Payments & Boosts
- [ ] Sprint 8: Testing & Monitoring
- [ ] Sprint 9: Ranking & Analytics
- [ ] Sprint 10: Polish & Launch Prep

## License

Proprietary - All Rights Reserved
