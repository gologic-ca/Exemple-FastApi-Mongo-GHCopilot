import pytest
from app.main import app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from models.profile import create_test_user, delete_test_user, follow_user
from utils.security import get_auth_headers


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_unfollow_user(client: TestClient):
    # Create a test user
    user = await create_test_user()

    # Follow the user
    await follow_user(user.username)

    # Unfollow the user
    response = await client.delete(
        f"/profiles/{user.username}/follow", headers=get_auth_headers()
    )
    assert response.status_code == 200

    # Check if the user is no longer following the other user
    assert user.following_ids == []

    # Check the response
    data = response.json()
    assert "profile" in data
    assert data["profile"]["following"] is False
    assert data["profile"]["username"] == user.username
    # Add more assertions as needed

    # Clean up
    await delete_test_user(user.username)


# Additional test case to cover the unfollow_user endpoint
@pytest.mark.asyncio
async def test_unfollow_user_endpoint(client: TestClient):
    # Create a test user
    user = await create_test_user()

    # Follow the user
    await follow_user(user.username)

    # Unfollow the user
    response = await client.delete(
        f"/profiles/{user.username}/follow", headers=get_auth_headers()
    )
    assert response.status_code == 200

    # Check if the user is no longer following the other user
    assert user.following_ids == []

    # Check the response
    data = response.json()
    assert "profile" in data
    assert data["profile"]["following"] is False
    assert data["profile"]["username"] == user.username
    # Add more assertions as needed

    # Clean up
    await delete_test_user(user.username)
