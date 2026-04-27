# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""Useful pytest fixtures"""

import os.path
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main, config, db

from tests import defaults


@pytest.fixture
def empty_db(tmp_path: str) -> str:
    """An empty database"""

    target_ouput = os.path.join(tmp_path, "empty.db")
    Path(target_ouput).touch()

    return target_ouput


@pytest.fixture
def valid_config_file(tmp_path: str, empty_db: str) -> str:
    """A standard config file pointing to an empty database"""

    target_output = os.path.join(tmp_path, "config.toml")
    with open(target_output, "w+", encoding="utf-8") as f:
        text = f"""
[database]
type = "sqlite"
path = "{tmp_path}/empty.db"
[auth]
jwt_secret="1bc4d545d9df425d833a636091957553"
jwt_algo="HS256"
token_lifetime=86400
"""
        f.write(text)

    return target_output


@pytest.fixture
def client(valid_config_file: str):
    """HTTP client"""

    config.manager.lookup_paths = [str(Path(valid_config_file).parent)]
    config.manager.reload()
    db.manager.reset()

    client = TestClient(main.create_app())

    # Populate the database with some defaults

    client.post("/profile", json=defaults.USER)

    yield client


@pytest.fixture
def token(client: TestClient) -> str:
    """Access token"""
    response = client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": defaults.USER["password"],
        },
    )

    token = response.json()["access_token"]
    return token


@pytest.fixture
def no_scope_token(client: TestClient) -> str:
    """Access token with a dummy scope"""
    return client.post(
        "/auth/token",
        data={
            "username": defaults.USER["username"],
            "password": defaults.USER["password"],
            "scope": "testing",
        },
    ).json()["access_token"]
