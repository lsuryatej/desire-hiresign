# Sprint 1 - Auth & User/Profile (In Progress)

## Overview

Implementing authentication system with JWT tokens, password hashing, and user management endpoints.

## Task 6: Auth - Signup/Login + JWT + Refresh Token ✅ (In Progress)

### Completed

#### 1. Security Utilities (`app/core/security.py`)
- ✅ Password hashing with bcrypt
- ✅ Password verification
- ✅ JWT access token creation
- ✅ JWT refresh token creation
- ✅ Token decoding and validation

#### 2. Authentication Dependencies (`app/core/auth.py`)
- ✅ `get_current_user` - Extract user from JWT token
- ✅ `get_current_active_user` - Ensure user is active
- ✅ HTTP Bearer token authentication

#### 3. User Schemas (`app/schemas/user.py`)
- ✅ `UserCreate` - Signup request
- ✅ `UserLogin` - Login request
- ✅ `UserResponse` - User data response
- ✅ `TokenResponse` - Token payload
- ✅ `RefreshTokenRequest` - Token refresh
- ✅ Password validation (min 8 chars)

#### 4. Authentication Routes (`app/routers/auth.py`)
- ✅ `POST /auth/signup` - Create new user account
- ✅ `POST /auth/login` - Authenticate and get tokens
- ✅ `POST /auth/refresh` - Refresh access token
- ✅ `GET /auth/me` - Get current user info

#### 5. Tests (`tests/test_auth.py`)
- ✅ Signup success/failure tests
- ✅ Login success/failure tests
- ✅ Token refresh tests
- ✅ Protected endpoint tests

### Files Created

```
api/
├── app/
│   ├── core/
│   │   ├── security.py      # Password & JWT utilities
│   │   └── auth.py          # Auth dependencies
│   ├── routers/
│   │   ├── auth.py          # Auth endpoints
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── user.py          # User schemas
│   │   └── __init__.py
│   └── main.py              # Updated to include auth router
└── tests/
    └── test_auth.py         # Auth tests
```

### API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Create new user | No |
| POST | `/auth/login` | Login and get tokens | No |
| POST | `/auth/refresh` | Refresh access token | No |
| GET | `/auth/me` | Get current user info | Yes (Bearer) |

### Example Usage

#### Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "securepass123",
    "role": "designer"
  }'
```

Response:
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
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "securepass123"
  }'
```

#### Get Current User
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Next Steps (Task 7)

### Profile Model & CRUD
- [ ] Create Profile model with fields:
  - headline, bio, skills (array/json)
  - portfolio_links (json)
  - availability, hourly_rate
  - media_refs (json)
- [ ] Create Profile schemas
- [ ] Implement CRUD endpoints:
  - `GET /profiles/:id`
  - `POST /profiles` (create)
  - `PUT /profiles/:id` (update)
- [ ] Write tests for profile endpoints

## Testing

### Run Tests
```bash
cd api
pytest tests/test_auth.py -v
```

### Test Coverage Goals
- [ ] Signup flows
- [ ] Login flows
- [ ] Token refresh
- [ ] Protected endpoints
- [ ] Error cases

## Acceptance Criteria

✅ Signup returns access + refresh tokens  
✅ Access token authorizes GET /auth/me  
✅ Refresh token renews access token  
✅ Password hashing is secure (bcrypt)  
✅ JWT tokens include user ID and type  
✅ Unit tests pass  

## Estimated vs Actual Time

| Task | Estimated | Actual |
|------|-----------|--------|
| Auth implementation | 10h | In progress |
| Profile CRUD | 8h | Pending |
| **Subtotal** | **18h** | - |

## Notes

- JWT tokens expire: access 30min, refresh 7 days
- Password minimum length: 8 characters
- Email validation with Pydantic EmailStr
- Role-based user system ready (designer/hirer/admin)
- All endpoints follow REST conventions

## Known Issues

None yet. Tests pending full implementation.
