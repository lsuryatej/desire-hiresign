# Sprint 1 Testing Notes

## Issues Found and Fixed

### Issue 5: Missing `bcrypt` dependency
**Error**: `ValueError: password cannot be longer than 72 bytes`
**Cause**: passlib bcrypt backend has issues with Python 3.13
**Fix**: Replaced passlib with direct bcrypt library usage in `api/app/core/security.py`

### Issue 6: JWT Subject Must Be String
**Error**: `Subject must be a string` when decoding JWT tokens
**Cause**: python-jose expects JWT subject ("sub") to be a string, but we were passing integers
**Fix**: 
- Updated `api/app/routers/auth.py` to convert user ID to string when creating tokens: `{"sub": str(user.id)}`
- Updated `api/app/core/auth.py` to convert back to int when querying: `User.id == int(user_id_str)`

### Additional Fixes Needed
- Updated `api/pyproject.toml` to use `bcrypt>=4.0.0` instead of `passlib[bcrypt]`

## Testing Results

### Successful Endpoints Tested:
1. ✅ POST /auth/signup - User registration with JWT tokens
2. ✅ POST /auth/login - User authentication  
3. ✅ GET /auth/me - Get current user info with authentication
4. ✅ POST /profiles - Create user profile
5. ✅ GET /profiles/me - Retrieve user's own profile

### Test Flow:
```
1. Sign up user → Receive access_token and refresh_token
2. Use access_token in Authorization header
3. Get current user info
4. Create profile
5. Retrieve profile
```

## Verification Commands

All endpoints are working correctly with proper JWT authentication.
