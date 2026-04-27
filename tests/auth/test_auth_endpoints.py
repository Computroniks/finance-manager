# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

from fastapi.testclient import TestClient
from fastapi import status

from app import config
from app.auth.flows import VALID_SCOPES
import jwt

from tests import defaults


def test_login(client: TestClient):
    """Test logging in with valid credentials"""

    response = client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": defaults.USER["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == config.manager.config.auth.token_lifetime
    assert len(data) == 3


def test_login_invalid_username(client: TestClient):
    """Test logging in with invalid username fails"""

    response = client.post(
        "/auth/token",
        data={
            "username": "an invalid username",
            "password": defaults.USER["password"],
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Failed to authenticate user"
    assert len(data) == 1


def test_login_invalid_password(client: TestClient):
    """Test logging in with invalid password fails"""

    response = client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": "a very wrong password",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Failed to authenticate user"
    assert len(data) == 1


def test_login_no_scopes(client: TestClient):
    """Password login with no scopes should give all the scopes"""

    response = client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": defaults.USER["password"],
        },
    ).json()

    scopes = jwt.decode(
        response["access_token"],
        key=config.manager.config.auth.jwt_secret,
        algorithms=config.manager.config.auth.jwt_algo,
    )["scope"].split(" ")

    assert len(scopes) == len(VALID_SCOPES)

    for scope in VALID_SCOPES:
        assert scope in scopes


def test_login_invalid_scope(client: TestClient):
    """An invalid scope should result in an error"""

    response = client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": defaults.USER["password"],
            "scope": ["qwerty"],
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
