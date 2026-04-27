# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Exceptions for user profiles

All exceptions inherit from fastapi.HTTPException, this is to allow
automatic generation of error responses. As such, care must be taken not
to include sensitive data in error messages. None of these exceptions
will cause the server to crash, they are only used to handle expected
request errors.
"""

from typing import Mapping

from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    """No user could be found with this ID"""

    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "User not found", headers)


class UserAlreadyExistsError(HTTPException):
    """A user already exists on the system with this username"""

    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "User already exists", headers)
