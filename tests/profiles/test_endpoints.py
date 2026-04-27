# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

from fastapi.testclient import TestClient
from fastapi import status

from tests import defaults


def test_create_user(client: TestClient):
    """Test creating a user succeeds"""

    user = {
        "username": "abc123",
        "name": "Example",
        "email": "example@example.com",
        "password": "abc123",
    }
    response = client.post("/profile", json=user)
    assert response.status_code == status.HTTP_201_CREATED

    response_user: dict[str, str] = response.json()
    assert response_user["username"] == user["username"]
    assert response_user["name"] == user["name"]
    assert response_user["email"] == user["email"]
    assert response_user["id"]
    assert len(response_user) == 4


def test_create_user_already_exists(client: TestClient):
    """Test duplicate usernames fail"""

    response = client.post("/profile", json=defaults.USER)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_profile(client: TestClient, token: str):
    """Getting profile should return the token user"""

    response = client.get("/profile", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    response_user = response.json()
    assert response_user["username"] == defaults.USER["username"]
    assert response_user["name"] == defaults.USER["name"]
    assert response_user["email"] == defaults.USER["email"]
    assert response_user["id"]
    assert len(response_user) == 4


def test_get_profile_missing_scope(client: TestClient, no_scope_token: str):
    """Getting a profile should fail for tokens without read:profile"""

    response = client.get(
        "/profile", headers={"Authorization": f"Bearer {no_scope_token}"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
