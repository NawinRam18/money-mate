from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register():
    response = client.post(
        "/api/v1/auth/register",
        params={
            "name": "Test User",
            "email": "test_user_12345@example.com",
            "phone": "9000000000",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["email"] == "test_user_12345@example.com"


def test_login():
    response = client.post(
        "/api/v1/auth/login",
        params={
            "email": "test_user_12345@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"