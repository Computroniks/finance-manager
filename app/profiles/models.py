# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""
Models for user profiles
"""

from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, EmailStr, Field

from app.db import Base


# pylint: disable-next=too-few-public-methods
class User(Base):
    """User database schema"""

    __tablename__ = "user"

    def __init__(self, **kw: Any):
        if "id" not in kw:
            kw["id"] = uuid4()
        super().__init__(**kw)

    pk: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class UserRead(BaseModel):
    """Schema for reading a user"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "8a42324f-c23b-4bb1-9a1b-fa9c90af9c39",
                    "name": "John Doe",
                    "username": "jdoe",
                    "email": "john@example.com",
                }
            ]
        }
    }

    id: UUID
    name: str
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    """Schema for creating a user"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "username": "jdoe",
                    "email": "john@example.com",
                    "password": "my-super-secret-password",
                }
            ]
        }
    }

    name: str
    username: str = Field(pattern=r"^[a-z0-9_]+$")
    email: EmailStr
    password: str


class UserPartialUpdate(BaseModel):
    """Schema for updating a user"""

    name: Optional[str]
    username: Optional[str] = Field(pattern=r"^[a-z0-9_]+$")
    email: Optional[str]
