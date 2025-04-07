import pytest
from fastapi.testclient import TestClient
from main import app
from odmantic.bson import ObjectId

from models.user import UserModel
from settings import Engine

client = TestClient(app)


@pytest.fixture
async def test_users():
    # Créer des utilisateurs de test
    users = [
        UserModel(
            username=f"test_user_{i}",
            email=f"test{i}@example.com",
            hashed_password="test_password",
            bio=f"Test bio {i}",
            image=f"https://example.com/image{i}.jpg",
        )
        for i in range(3)
    ]
    for user in users:
        await Engine.save(user)
    return users


@pytest.mark.asyncio
async def test_get_profiles_list(test_users):
    response = client.get("/profiles")
    assert response.status_code == 200
    data = response.json()
    assert "profiles" in data
    assert len(data["profiles"]) == 3

    # Vérifier la structure de chaque profil
    for profile in data["profiles"]:
        assert "username" in profile
        assert "bio" in profile
        assert "image" in profile
        assert "following" in profile
        assert isinstance(profile["following"], bool)


@pytest.mark.asyncio
async def test_get_profiles_list_with_auth(test_users):
    # Créer un utilisateur connecté
    logged_user = UserModel(
        username="logged_user",
        email="logged@example.com",
        hashed_password="test_password",
        following_ids=(test_users[0].id,),
    )
    await Engine.save(logged_user)

    # Simuler la connexion
    response = client.get("/profiles", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["profiles"]) == 3

    # Vérifier que following est correctement défini
    for profile in data["profiles"]:
        if profile["username"] == test_users[0].username:
            assert profile["following"] is True
        else:
            assert profile["following"] is False
