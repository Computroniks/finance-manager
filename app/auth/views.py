# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
HTTP endpoints for auth.

Includes all endpoints under the /auth prefix.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db import DBSession

from .models import Token
from .flows import password_token_request

router = APIRouter(prefix="/auth")


@router.post("/token", tags=["auth"])
async def token(
    db: DBSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Retrieve a token through the password flow.

    Args:
        db: DB session
        form_data: Username, password and scope information

    Returns:
        Access token
    """

    return password_token_request(
        db, form_data.username, form_data.password, form_data.scopes
    )
