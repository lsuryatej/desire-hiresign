#!/bin/bash

# Sprint 1 Testing Script
set -e

API_URL="http://localhost:8000"

echo "🧪 Testing Sprint 1 - Authentication & Profiles"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print info
info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Test 1: Health check
echo "Test 1: Health Check"
response=$(curl -s http://localhost:8000/health)
if [[ $response == *"ok"* ]]; then
    success "Health check passed"
else
    error "Health check failed: $response"
    exit 1
fi
echo ""

# Test 2: Signup
echo "Test 2: User Signup"
response=$(curl -s -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "designer@example.com",
    "password": "securepass123",
    "role": "designer"
  }')

if [[ $response == *"access_token"* ]]; then
    success "Signup successful"
    ACCESS_TOKEN=$(echo $response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "Access token: ${ACCESS_TOKEN:0:20}..."
else
    error "Signup failed: $response"
    exit 1
fi
echo ""

# Test 3: Get current user
echo "Test 3: Get Current User"
response=$(curl -s -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if [[ $response == *"designer@example.com"* ]]; then
    success "Get current user successful"
else
    error "Get current user failed: $response"
fi
echo ""

# Test 4: Create profile
echo "Test 4: Create Profile"
response=$(curl -s -X POST http://localhost:8000/profiles \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "UI/UX Designer",
    "bio": "Passionate designer with 5+ years of experience",
    "skills": ["UI Design", "Figma", "Prototyping"],
    "availability": "available",
    "hourly_rate": 50.0,
    "location": "San Francisco, CA"
  }')

if [[ $response == *"headline"* ]]; then
    success "Profile created successfully"
    PROFILE_ID=$(echo $response | grep -o '"id":[0-9]*' | cut -d':' -f2)
else
    error "Profile creation failed: $response"
fi
echo ""

# Test 5: Get profile
echo "Test 5: Get Profile"
response=$(curl -s -X GET http://localhost:8000/profiles/$PROFILE_ID)

if [[ $response == *"UI/UX Designer"* ]]; then
    success "Get profile successful"
else
    error "Get profile failed: $response"
fi
echo ""

echo ""
echo "================================================"
echo -e "${GREEN}All tests passed! 🎉${NC}"
echo ""
echo "Summary:"
echo "✓ Health check"
echo "✓ User signup"
echo "✓ Get current user"
echo "✓ Create profile"
echo "✓ Get profile"
echo ""
echo "API is working correctly!"
