# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""Auth services"""

from typing import Any
from datetime import timedelta, datetime, timezone

import jwt
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session

from app import config
from app.profiles.models import User
from app.profiles.service import get_user_by_name
from app.profiles.exceptions import UserNotFoundError
from app.crypt import verify_password


from .models import TokenData
from .exceptions import AuthenticationFailedError, MalformedTokenError


def create_access_token(data: TokenData, expires_delta: timedelta) -> str:
    """
    Create an access token from provided data

    Create and sign an access token with the provided scopes and lifetime

    Args:
        data: Token data to include
        expires_delta: Lifetime of token

    Returns:
        Signed and encoded JWT token
    """

    expire = datetime.now(timezone.utc) + expires_delta
    raw_data: dict[str, Any] = {
        "sub": str(data.user_id),
        "scope": " ".join(data.scopes),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(  # type: ignore
        raw_data,
        key=config.manager.config.auth.jwt_secret,
        algorithm=config.manager.config.auth.jwt_algo,
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decode a provided access token

    Will verify the signature of an access token and return it's data

    Args:
        token: Token to decode

    Raises:
        AuthenticationFailedError: The token could not be verified
        MalformedTokenError: The token was missing the subject field
        MalformedTokenError: The token was missing the scope field

    Returns:
        Token contents
    """

    try:
        payload = jwt.decode(  # type: ignore
            token,
            config.manager.config.auth.jwt_secret,
            algorithms=[config.manager.config.auth.jwt_algo],
        )
    except jwt.InvalidTokenError as e:
        raise AuthenticationFailedError from e

    user_id = payload.get("sub")
    if user_id is None:
        raise MalformedTokenError("missing field `sub`")

    raw_scopes = payload.get("scope")
    if raw_scopes is None:
        raise MalformedTokenError("missing field `scope`")

    scopes = str(raw_scopes).split(" ")

    return TokenData(user_id=user_id, scopes=scopes)


def token_has_access(
    required_scopes: SecurityScopes, provided_scopes: list[str]
) -> bool:
    """
    Check if the provided scopes have required level of access.

    Ensures that all the required scopes exist in the provided scopes.

    Args:
        required_scopes: Scopes required to access the resource
        provided_scopes: Scopes contained in the token.

    Returns:
        True if the token has access
    """

    for scope in required_scopes.scopes:
        if scope not in provided_scopes:
            return False

    return True


def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Verify a username and password pair

    Will attempt to look user up in database and verify their password.
    If the user is not found in the database, will attempt to verify a
    dummy password as a countermeasure against timing attacks.

    Args:
        db: Database session
        username: Username of user to lookup
        password: Password to authenticate with

    Raises:
        AuthenticationFailedError: The user was not found
        AuthenticationFailedError: The password could not be verified

    Returns:
        The user authenticated by the username password pair
    """

    try:
        user = get_user_by_name(db, username)
    except UserNotFoundError as e:
        # Verify a dummy password to avoid timing attacks
        verify_password(
            "a dummy password",
            "$2b$12$KBikqteDuT79adoU2g2S2OVjE8UtCjoPSzNj8In3.mE4yayQ6Y/Mq",  # another dummy password
        )
        raise AuthenticationFailedError from e

    if not verify_password(password, user.password):
        raise AuthenticationFailedError

    return user
