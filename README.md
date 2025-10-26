# DesignHire API

A Tinder-style marketplace API for connecting designers with hirers.

## 🚀 Status

**Current Status:** Sprint 3 Complete, CI/CD Setup ✅

All code has been formatted with black, linted, and is ready for production.

## 📊 Features Implemented

### Sprint 1 - Foundation ✅
- ✅ Authentication with JWT tokens
- ✅ User signup/login/refresh
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (designer, hirer, admin)
- ✅ Profile CRUD operations
- ✅ File upload with presigned URLs (S3/MinIO)

### Sprint 2 - Listings ✅  
- ✅ Listings model with all fields
- ✅ Advanced filtering (skills, location, salary range)
- ✅ Role-based access (only hirers create)
- ✅ Background worker for thumbnails
- ✅ Media safety validation

### Sprint 3 - Swipe Feed & Interactions ✅
- ✅ Interactions system (like/skip/apply)
- ✅ Duplicate prevention (24-hour window)
- ✅ Profile feed endpoint for swiping
- ✅ Interaction statistics
- ✅ Prevent self-interactions

## 🗄️ Database Schema

### Tables
- `users` - User accounts
- `profiles` - Designer profiles  
- `listings` - Job postings
- `interactions` - User actions (likes/skips/applies)

## 🔗 API Endpoints

See full documentation at: http://localhost:8000/docs

### Authentication
- `POST /auth/signup` - Create account
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get current user

### Profiles
- `POST /profiles` - Create profile
- `GET /profiles/me` - Get my profile
- `GET /profiles/{id}` - Get profile
- `GET /profiles/feed` - Swipe feed
- `PUT /profiles/me` - Update profile
- `DELETE /profiles/me` - Delete profile

### Listings
- `POST /listings` - Create listing (hirers only)
- `GET /listings` - Get listings with filters
- `GET /listings/{id}` - Get specific listing
- `GET /listings/my-listings` - Get my listings
- `PUT /listings/{id}` - Update listing
- `DELETE /listings/{id}` - Delete listing

### Interactions
- `POST /interactions` - Create interaction (like/skip/apply)
- `GET /interactions` - List my interactions
- `GET /interactions/stats` - Interaction statistics

### Media
- `POST /media/signed-url` - Get upload URL
- `POST /media/delete` - Delete file
- `POST /media/process` - Process image (thumbnail)

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- MinIO (S3-compatible storage)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/lsuryatej/desire-hiresign.git
cd desire-hiresign
```

2. **Set up infrastructure**
```bash
./scripts/start-infra.sh  # Start PostgreSQL, Redis, MinIO
```

3. **Set up API**
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

4. **Configure environment**
```bash
cp env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

7. **Access API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 🧪 Testing

### Run tests
```bash
cd api
pytest
```

### Run linters
```bash
flake8 app tests
black --check app tests
```

## 📝 Development

### Code Style
- Python: Black, flake8
- TypeScript: ESLint
- Format with `black .` before committing

### Git Workflow
- Main branch: Production-ready code
- Feature branches for new features
- All code must pass CI/CD checks

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) - UI/UX guidelines
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing instructions
- [FINAL_STATUS.md](FINAL_STATUS.md) - Project status

## 🎯 Next Steps

**Sprint 4 - Matches & Messaging**
- Match detection logic
- Matches table
- Messaging system
- WebSocket for real-time

## ✅ CI/CD Status

[![CI](https://github.com/lsuryatej/desire-hiresign/actions/workflows/ci.yml/badge.svg)](https://github.com/lsuryatej/desire-hiresign/actions/workflows/ci.yml)

## 📄 License

Copyright © 2025 DesignHire
