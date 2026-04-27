# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Cryptography related functions used across the code base.
"""

import base64
import hashlib

import bcrypt


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password with a hash

    Args:
        plain: Plain text password to verify
        hashed: Stored hash of correct password

    Returns:
        True if password is valid
    """

    plain_256 = base64.b64encode(hashlib.sha256(plain.encode()).digest())
    return bcrypt.checkpw(plain_256, hashed.encode())


def hash_password(password: str) -> bytes:
    """
    Hash the provided password and return the bytes.

    Uses bcrypt underneath but avoids length limit by pre-hashing the
    input.

    Args:
        password: Password to hash

    Returns:
        Hashed bytes
    """

    return bcrypt.hashpw(
        base64.b64encode(hashlib.sha256(password.encode()).digest()),
        bcrypt.gensalt(),
    )
