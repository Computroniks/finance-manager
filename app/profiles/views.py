# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""User management endpoints"""

from typing import Annotated

from fastapi import APIRouter, Security, status

from app.auth.flows import get_current_user
from app.db import DBSession
from app.models import HttpError

from .models import User, UserRead, UserCreate
from .service import create_user

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserRead)
async def get_profile(
    user: Annotated[User, Security(get_current_user, scopes=["read:profile"])],
):
    """
    Get the profile of the currently authenticated user

    Will read the provided access token to retrieve user ID and return
    the appropriate user. Requires the `read:profile` scope.
    """

    return user


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    responses={
        409: {
            "model": HttpError,
            "description": "User already exists",
        }
    },
)
async def create_account(db: DBSession, user: UserCreate):
    """Create a new user account"""
    return create_user(db, user)
