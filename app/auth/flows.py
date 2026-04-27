# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Authentication flows and related auth settings.

This package contains the authentication flows, e.g. token flows,
getting the currently logged in user and so on, in addition to the OAuth
schemes used by the application.
"""

from datetime import timedelta
from typing import Annotated
import os

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.db import DBSession
from app import config
from app.profiles.service import get_user_by_id
from app.profiles.exceptions import UserNotFoundError
from app.profiles.models import User

from . import service
from .exceptions import (
    InsufficientScopeError,
    InvalidScopeError,
    InvalidTokenError,
)
from .models import TokenData, Token


VALID_SCOPES = {
    "read:profile": "Read your user profile",
    "write:profile": "Update your user profile",
}

if os.getenv("DEBUG"):
    VALID_SCOPES["testing"] = "Testing scope. Does nothing."

OAUTH_PWD_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token", scopes=VALID_SCOPES)

BearerToken = Annotated[str, Depends(OAUTH_PWD_SCHEME)]


def password_token_request(
    db: DBSession, username: str, password: str, requested_scopes: list[str]
) -> Token:
    """
    Handle token requests with the password flow.

    Will attempt to log a user in with a username and password. If no
    scopes are requested, all valid scopes will be included with the
    token.

    Args:
        db: Database session
        username: Username of user to attempt login
        password: Password of user to attempt login
        requested_scopes: List of scopes requested

    Raises:
        InvalidScopeError: A scope was requested that was not recognised

    Returns:
        Access token
    """

    user = service.authenticate_user(db, username, password)
    access_token_expires = timedelta(seconds=config.manager.config.auth.token_lifetime)

    token_scopes: list[str] = []
    if requested_scopes and len(requested_scopes) > 0:
        for scope in requested_scopes:
            if scope in VALID_SCOPES:
                token_scopes.append(scope)
            else:
                raise InvalidScopeError(scope)
    else:
        token_scopes = list(VALID_SCOPES.keys())

    access_token = service.create_access_token(
        TokenData(user_id=user.id, scopes=token_scopes), access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )


async def get_current_user(
    db: DBSession,
    security_scopes: SecurityScopes,
    token: BearerToken,
) -> User:
    """
    Get the currently logged in user

    Args:
        db: Database session
        security_scopes: Required scopes for access to calling resource
        token: Token provided by caller

    Raises:
        AuthenticationFailedError: The user identified by the token could not be found
        AuthenticationFailedError: The user identified by the token is not active
        InsufficientScopeError: The token does not have the required scope
        to access the resource

    Returns:
        Calling user identified by the access token
    """

    decoded_token = service.decode_access_token(token)

    try:
        user = get_user_by_id(db, decoded_token.user_id)
    except UserNotFoundError as e:
        raise InvalidTokenError from e

    if not user.active:
        raise InvalidTokenError

    if not service.token_has_access(security_scopes, decoded_token.scopes):
        raise InsufficientScopeError

    return user
