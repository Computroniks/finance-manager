# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""Authentication models"""

from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    """
    Access token response model

    Attributes:
        access_token: The encoded JWT access token
        token_type: This will always be bearer
        expires_in: Number of seconds the token is valid for
    """

    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """
    Data included in the encoded JWT

    Attributes:
        user_id: UUID of user
        scopes: List of scopes the token is valid for
    """

    user_id: UUID
    scopes: list[str]
