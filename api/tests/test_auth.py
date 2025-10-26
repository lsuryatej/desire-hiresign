import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User, UserRole
from app.core.security import get_password_hash

client = TestClient(app)


@pytest.fixture
def test_user_data():
    return {"email": "test@example.com", "password": "testpass123", "role": "designer"}


@pytest.fixture
def created_user(db_session: Session, test_user_data):
    hashed_password = get_password_hash(test_user_data["password"])
    user = User(
        email=test_user_data["email"], password_hash=hashed_password, role=UserRole.DESIGNER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_signup_success(test_user_data):
    """Test successful user signup."""
    response = client.post("/auth/signup", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["role"] == test_user_data["role"]


def test_signup_duplicate_email(test_user_data, created_user):
    """Test signup with existing email fails."""
    response = client.post("/auth/signup", json=test_user_data)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_invalid_password(test_user_data):
    """Test signup with invalid password."""
    test_user_data["password"] = "short"  # Too short
    response = client.post("/auth/signup", json=test_user_data)

    assert response.status_code == 422  # Validation error


def test_login_success(test_user_data, created_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == test_user_data["email"]


def test_login_wrong_password(test_user_data, created_user):
    """Test login with wrong password."""
    response = client.post(
        "/auth/login", json={"email": test_user_data["email"], "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login", json={"email": "nonexistent@example.com", "password": "anypassword"}
    )

    assert response.status_code == 401


def test_refresh_token(test_user_data, created_user):
    """Test token refresh."""
    # First login
    login_response = client.post(
        "/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]},
    )
    refresh_token = login_response.json()["refresh_token"]

    # Refresh
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_refresh_invalid_token():
    """Test refresh with invalid token."""
    response = client.post("/auth/refresh", json={"refresh_token": "invalid_token"})

    assert response.status_code == 401


def test_get_current_user(test_user_data, created_user):
    """Test getting current user info."""
    # Login
    login_response = client.post(
        "/auth/login",
        json={"email": test_user_data["email"], "password": test_user_data["password"]},
    )
    access_token = login_response.json()["access_token"]

    # Get current user
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]


def test_get_current_user_no_token():
    """Test getting current user without token."""
    response = client.get("/auth/me")

    # FastAPI returns 403 for missing credentials
    assert response.status_code in [401, 403]


def test_get_current_user_invalid_token():
    """Test getting current user with invalid token."""
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 401
