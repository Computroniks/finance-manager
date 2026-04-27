# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Test cases for auth exceptions.
"""

from fastapi import status

from app.auth.exceptions import (
    AuthenticationFailedError,
    InvalidTokenError,
    InvalidScopeError,
    MalformedTokenError,
    InsufficientScopeError,
)


def test_auth_failed():
    """Test auth failed message and code"""
    exception = AuthenticationFailedError()

    assert exception.detail == "Failed to authenticate user"
    assert exception.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_token():
    """Test invalid token message and code"""
    exception = InvalidTokenError()

    assert exception.detail == "Invalid token"
    assert exception.status_code == status.HTTP_403_FORBIDDEN


def test_malformed_token_no_msg():
    """Test malformed token without message"""
    exception = MalformedTokenError()

    assert exception.detail == "Provided token is malformed"
    assert exception.status_code == status.HTTP_400_BAD_REQUEST


def test_malformed_token_msg():
    """Test malformed token with message"""
    exception = MalformedTokenError(detail="abc123")

    assert exception.detail == "Provided token is malformed: abc123"
    assert exception.status_code == status.HTTP_400_BAD_REQUEST


def test_insufficient_scope():
    """Test insufficient scope status and detail"""
    exception = InsufficientScopeError()

    assert exception.detail == "Insufficient scope to access resource"
    assert exception.status_code == status.HTTP_403_FORBIDDEN


def test_invalid_scope():
    """Test malformed token without message"""
    exception = InvalidScopeError(scope="abc123")

    assert exception.detail == "Scope abc123 is not recognised as a valid scope"
    assert exception.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
