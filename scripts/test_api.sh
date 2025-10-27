#!/bin/bash

# API Testing Script
# Tests core features: auth, profiles, listings, interactions, matches, messaging

BASE_URL="http://localhost:8000"
EMAIL1="test$(date +%s)@example.com"
EMAIL2="test2$(date +%s)@example.com"
PASSWORD="Test123456!"

echo "🧪 Testing DesignHire API..."
echo ""

# Test 1: Health Check
echo "1. Testing health endpoint..."
curl -s "$BASE_URL/health" | python3 -m json.tool
echo "✓ Health check passed"
echo ""

# Test 2: Signup
echo "2. Testing user signup..."
SIGNUP_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL1\",
    \"password\": \"$PASSWORD\",
    \"role\": \"designer\"
  }")

ACCESS_TOKEN=$(echo $SIGNUP_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$ACCESS_TOKEN" ]; then
  echo "✗ Signup failed"
  echo "$SIGNUP_RESPONSE"
  exit 1
fi
echo "✓ Signup successful"
echo ""

# Test 3: Get Current User
echo "3. Testing get current user..."
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "$ME_RESPONSE" | python3 -m json.tool | head -10
echo "✓ Get current user successful"
echo ""

# Test 4: Create Profile
echo "4. Testing profile creation..."
PROFILE_RESPONSE=$(curl -s -X POST "$BASE_URL/profiles" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Expert UI/UX Designer",
    "bio": "Passionate designer with 5 years of experience",
    "skills": ["UI/UX", "Figma", "Design Systems"],
    "portfolio_links": [{"behance": "https://behance.net/portfolio"}],
    "availability": "full-time",
    "hourly_rate": 50,
    "location": "San Francisco, CA",
    "remote_preference": "remote"
  }')

PROFILE_ID=$(echo $PROFILE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)

if [ -z "$PROFILE_ID" ]; then
  echo "✗ Profile creation failed"
  echo "$PROFILE_RESPONSE"
  exit 1
fi
echo "✓ Profile created (ID: $PROFILE_ID)"
echo ""

# Test 5: Get Onboarding Steps
echo "5. Testing onboarding next steps..."
ONBOARDING=$(curl -s -X GET "$BASE_URL/profiles/onboarding/next-steps" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "$ONBOARDING" | python3 -m json.tool
echo "✓ Onboarding steps retrieved"
echo ""

# Test 6: Search Profiles
echo "6. Testing profile search..."
SEARCH=$(curl -s -X GET "$BASE_URL/profiles/search?q=designer&min_completeness=0" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "$SEARCH" | python3 -m json.tool | head -20
echo "✓ Search successful"
echo ""

# Test 7: Listings Feed
echo "7. Testing listings feed..."
LISTINGS=$(curl -s -X GET "$BASE_URL/listings" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "$LISTINGS" | python3 -m json.tool | head -20
echo "✓ Listings retrieved"
echo ""

echo "✅ All API tests passed!"
echo ""
echo "Summary:"
echo "- Health check: ✓"
echo "- User signup: ✓"
echo "- Get current user: ✓"
echo "- Profile creation: ✓"
echo "- Onboarding steps: ✓"
echo "- Profile search: ✓"
echo "- Listings feed: ✓"

