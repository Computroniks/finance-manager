# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""User account management services"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError

from app.db import DBSession
from app.crypt import hash_password

from .models import User, UserCreate
from .exceptions import UserNotFoundError, UserAlreadyExistsError


def get_user_by_name(db: Session, username: str) -> User:
    """
    Get a user by their username

    Will error if no account could be found.

    Args:
        db: Database session
        username: Username to lookup

    Returns:
        Complete user
    """

    stmt = select(User).where(User.username == username)
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound as e:
        raise UserNotFoundError from e

    return result


def get_user_by_id(db: Session, user_id: UUID) -> User:
    """
    Find a user by their ID

    Will attempt to find a user in the database based upon their ID. If
    no user matching the ID can be found an exception will be raised.

    Args:
        db: Database session
        user_id: UUID of user to lookup

    Raises:
        UserNotFoundError: No user with matching UUID could be found

    Returns:
        User by UUID
    """

    stmt = select(User).where(User.id == user_id)
    try:
        result = db.execute(stmt).scalar_one()
    except NoResultFound as e:
        raise UserNotFoundError from e

    return result


def create_user(db: DBSession, user: UserCreate) -> User:
    """
    Create a user

    Create a user based upon a client submission. If the user already
    exists in the database an exception will be thrown. NOTE: There is a
    minute possibility that two users with different usernames would
    result in a duplicate being detected, this would only occur if there
    was a UUID collision. As such, we can assume this will not occur.

    Args:
        db: Database session
        user: User to create

    Raises:
        UserAlreadyExistsError: A user with this username already exists
        in the database.

    Returns:
        The newly created user.
    """

    user.password = hash_password(user.password).decode("utf-8")
    db_user = User(**user.model_dump())

    db_user.active = True

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise UserAlreadyExistsError from e

    return db_user
