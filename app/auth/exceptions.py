# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Exceptions for authentication

All exceptions inherit from fastapi.HTTPException, this is to allow
automatic generation of error responses. As such, care must be taken not
to include sensitive data in error messages. None of these exceptions
will cause the server to crash, they are only used to handle expected
request errors.
"""

from typing import Mapping

from fastapi import HTTPException, status


class AuthenticationFailedError(HTTPException):
    """
    Failed to authenticate a user

    This is because of an invalid username or password, although we will
    not reveal to the user which is the case.
    """

    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED, "Failed to authenticate user", headers
        )


class MalformedTokenError(HTTPException):
    """The access token could not be read because it is malformed"""

    def __init__(
        self, detail: str | None = None, headers: Mapping[str, str] | None = None
    ) -> None:
        msg = "Provided token is malformed"
        if detail is not None:
            msg += f": {detail}"
        super().__init__(status.HTTP_400_BAD_REQUEST, msg, headers)


class InsufficientScopeError(HTTPException):
    """The provided token does not have the required scope for access"""

    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            "Insufficient scope to access resource",
            headers,
        )


class InvalidScopeError(HTTPException):
    """The requested scope was not recognised"""

    def __init__(self, scope: str, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Scope {scope} is not recognised as a valid scope",
            headers,
        )
