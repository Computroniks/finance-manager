# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

from app.crypt import hash_password, verify_password


def test_hash_verify() -> None:
    """Hashing and then verifying should match"""

    hashed_pwd = hash_password("abc123").decode("utf-8")
    assert verify_password("abc123", hashed_pwd)


def test_hash_diff() -> None:
    """Different passwords shouldn't match"""

    hashed_pwd = hash_password("abc123").decode("utf-8")
    assert not verify_password("qwerty", hashed_pwd)


def test_hash_long_pwd() -> None:
    """Passwords greater than 72 characters should be supported"""
    pwd = "abc" * 72
    assert len(pwd) > 72

    hashed_pwd = hash_password(pwd).decode("utf-8")
    assert hashed_pwd

    assert verify_password(pwd, hashed_pwd)

    # Also check it isn't just truncating it
    first_72 = pwd[:72]
    assert len(first_72) == 72
    assert not verify_password(first_72, hashed_pwd)
