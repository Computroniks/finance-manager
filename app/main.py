# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Main server entry point
"""

from fastapi import FastAPI

from app.config import manager
from app.openapi import OPENAPI_DOCS  # type: ignore
from app import db, accounts, profiles, auth


def create_app() -> FastAPI:
    """
    Create a new app instance

    Returns:
        The app
    """
    manager.reload()
    db.manager.init_db()
    app = FastAPI(**OPENAPI_DOCS)  # type: ignore

    app.include_router(accounts.router)
    app.include_router(auth.router)
    app.include_router(profiles.router)

    return app
