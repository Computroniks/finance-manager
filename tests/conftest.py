# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""Useful pytest fixtures"""

import os.path
from pathlib import Path

import pytest


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
"""
        f.write(text)

    return target_output
