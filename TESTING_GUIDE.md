# Testing Guide - Sprint 1

Complete guide to test authentication and profiles functionality.

## Prerequisites

1. Start infrastructure services
2. Setup API environment
3. Run database migrations

## Setup Instructions

### 1. Start Infrastructure

```bash
# From project root
docker-compose -f infra/docker-compose.yml up -d
```

Verify services are running:
```bash
docker ps
```

### 2. Setup API

```bash
cd api

# Create virtual environment (if not exists)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp env.example .env

# Run migrations
alembic upgrade head
```

### 3. Start API Server

```bash
cd api
source venv/bin/activate
uvicorn app.main:app --reload
```

API will be available at: `http://localhost:8000`

## Manual Testing

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "service": "designhire-api"}
```

### Test 2: API Documentation

Open in browser: `http://localhost:8000/docs`

You should see:
- Swagger UI with all endpoints
- Auth section with signup/login endpoints
- Profiles section with CRUD endpoints

### Test 3: User Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "securepass123",
    "role": "designer"
  }'
```

Expected response (201):
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "designer@example.com",
    "role": "designer",
    "is_active": true,
    "created_at": "...",
    "updated_at": "..."
  }
}
```

Save the `access_token` for next requests!

### Test 4: User Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "securepass123"
  }'
```

Expected: Same token response as signup

### Test 5: Get Current User

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Replace `YOUR_ACCESS_TOKEN` with token from signup/login.

Expected response (200):
```json
{
  "id": 1,
  "email": "designer@example.com",
  "role": "designer",
  "is_active": true,
  "created_at": "...",
  "updated_at": "..."
}
```

### Test 6: Create Profile

```bash
curl -X POST http://localhost:8000/profiles \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "UI/UX Designer",
    "bio": "Passionate designer with 5+ years of experience",
    "skills": ["UI Design", "Figma", "Prototyping"],
    "portfolio_links": [
      {"url": "https://behance.net/username", "title": "Behance Portfolio"}
    ],
    "availability": "available",
    "hourly_rate": 50.0,
    "location": "San Francisco, CA",
    "remote_preference": "remote"
  }'
```

Expected response (201):
```json
{
  "id": 1,
  "user_id": 1,
  "headline": "UI/UX Designer",
  "bio": "Passionate designer...",
  "skills": ["UI Design", "Figma", "Prototyping"],
  "portfolio_links": [...],
  "availability": "available",
  "hourly_rate": 50.0,
  "location": "San Francisco, CA",
  "remote_preference": "remote",
  "media_refs": {},
  "is_active": true,
  "completeness_score": 80,
  "created_at": "...",
  "updated_at": "..."
}
```

Note the `completeness_score` is calculated automatically!

### Test 7: Get My Profile

```bash
curl -X GET http://localhost:8000/profiles/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected: Your profile data

### Test 8: Update Profile

```bash
curl -X PUT http://localhost:8000/profiles/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Senior UI/UX Designer",
    "hourly_rate": 75.0
  }'
```

Expected: Updated profile with new headline and rate

### Test 9: Get Profile by ID

```bash
curl -X GET http://localhost:8000/profiles/1
```

Expected: Public profile data (no auth required)

### Test 10: Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

Expected: New access token

## Automated Testing

### Run All Tests

```bash
cd api
source venv/bin/activate
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

Open `htmlcov/index.html` to see coverage report.

## Error Testing

### Test 1: Signup with Existing Email

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "password123",
    "role": "designer"
  }'
```

Expected: 400 Bad Request - "Email already registered"

### Test 2: Login with Wrong Password

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "wrongpassword"
  }'
```

Expected: 401 Unauthorized - "Incorrect email or password"

### Test 3: Access Protected Endpoint Without Token

```bash
curl -X GET http://localhost:8000/auth/me
```

Expected: 401 Unauthorized

### Test 4: Access Protected Endpoint with Invalid Token

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer invalid_token_here"
```

Expected: 401 Unauthorized

### Test 5: Create Profile Without Authentication

```bash
curl -X POST http://localhost:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{"headline": "Test"}'
```

Expected: 401 Unauthorized

## Database Verification

### Check PostgreSQL

```bash
docker exec -it designhire-postgres psql -U postgres -d app
```

SQL Commands:
```sql
-- List all users
SELECT id, email, role, is_active FROM users;

-- List all profiles
SELECT id, user_id, headline, completeness_score FROM profiles;

-- Exit
\q
```

## Cleanup

### Reset Database

```bash
cd api
source venv/bin/activate
alembic downgrade base
alembic upgrade head
```

### Stop Services

```bash
docker-compose -f infra/docker-compose.yml down
```

## Success Checklist

- [ ] Health check returns OK
- [ ] API docs accessible at /docs
- [ ] Signup creates user and returns tokens
- [ ] Login returns tokens
- [ ] /auth/me returns user info
- [ ] Create profile works
- [ ] Get profile works
- [ ] Update profile works
- [ ] Refresh token works
- [ ] Error cases return proper status codes
- [ ] All pytest tests pass

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database connection error
```bash
# Check if postgres is running
docker ps | grep postgres

# Restart docker compose
docker-compose -f infra/docker-compose.yml restart
```

### Migration errors
```bash
cd api
alembic downgrade base
alembic upgrade head
```

## Next Steps

After testing Sprint 1:
1. File upload with signed URLs (MinIO)
2. Mobile profile creation flow
3. Background worker for thumbnails
