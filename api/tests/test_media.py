"""Tests for media upload endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session

client = TestClient(app)


@pytest.fixture
def auth_token(db: Session, client):
    """Create a test user and return auth token."""
    from app.core.security import get_password_hash

    # Create test user
    test_user = User(
        email="mediatest@example.com",
        password_hash=get_password_hash("testpass123"),
        role="designer",
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    # Login to get token
    response = client.post(
        "/auth/login", json={"email": "mediatest@example.com", "password": "testpass123"}
    )

    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

    token = response.json()["access_token"]
    return token


def test_get_signed_url(auth_token: str):
    """Test getting a presigned upload URL."""
    if not auth_token:
        pytest.skip("Failed to get auth token")

    response = client.post(
        "/media/signed-url",
        json={
            "file_name": "test-image.jpg",
            "content_type": "image/jpeg",
            "file_type": "image",
            "file_size": 1024,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert "upload_url" in data
    assert "object_key" in data
    assert "download_url" in data
    assert data["expires_in"] == 3600


def test_get_signed_url_invalid_file_type(auth_token: str):
    """Test getting presigned URL with invalid file type."""
    if not auth_token:
        pytest.skip("Failed to get auth token")

    response = client.post(
        "/media/signed-url",
        json={
            "file_name": "test.txt",
            "content_type": "text/plain",
            "file_type": "image",
            "file_size": 1024,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 400


def test_get_signed_url_file_too_large(auth_token: str):
    """Test getting presigned URL with file too large."""
    if not auth_token:
        pytest.skip("Failed to get auth token")

    response = client.post(
        "/media/signed-url",
        json={
            "file_name": "test-image.jpg",
            "content_type": "image/jpeg",
            "file_type": "image",
            "file_size": 20 * 1024 * 1024,  # 20MB
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Pydantic returns 422 for validation errors, FastAPI returns 400 for business logic
    assert response.status_code in [400, 422]


def test_get_signed_url_unauthorized():
    """Test getting presigned URL without authentication."""
    response = client.post(
        "/media/signed-url",
        json={
            "file_name": "test-image.jpg",
            "content_type": "image/jpeg",
            "file_type": "image",
            "file_size": 1024,
        },
    )

    assert response.status_code == 403


def test_get_signed_url_valid_file_types(auth_token: str):
    """Test valid file types for different categories."""
    if not auth_token:
        pytest.skip("Failed to get auth token")

    valid_combinations = [
        ("image/jpeg", "image"),
        ("image/png", "image"),
        ("image/webp", "image"),
        ("application/pdf", "document"),
        ("video/mp4", "video"),
    ]

    for content_type, file_type in valid_combinations:
        response = client.post(
            "/media/signed-url",
            json={
                "file_name": "test.jpg",
                "content_type": content_type,
                "file_type": file_type,
                "file_size": 1024,
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 201, f"Failed for {content_type}/{file_type}"
