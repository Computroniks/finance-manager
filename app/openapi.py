# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Configuration for OpenAPI docs portal.

Example:
from app.openapi import OPENAPI_DOCS

app = FastAPI(**OPENAPI_DOCS)
"""

from app import __version__

_TAGS_METADATA = [
    {
        "name": "auth",
        "description": "Login logic including authentication and token "
        + "retrieval. This does not include user management",
    },
    {"name": "profile", "description": "User account operations."},
]

OPENAPI_DOCS = {  # type: ignore
    "title": "Finance Manager",
    "version": __version__,
    "summary": "A comprehensive personal finance management system.",
    "openapi_tags": _TAGS_METADATA,
}
