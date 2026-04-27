# SPDX-FileCopyrightText: 2026 Zoe Nickson <zoe.nickson@sidingsmedia.com>
# SPDX-License-Identifier: MIT

"""Database handling for the application"""

import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, Session

from app import config

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base error for the database"""


class UnsupportedDatabaseError(DatabaseError):
    """The requested database is not supported"""


# pylint: disable-next=too-few-public-methods
class Base(DeclarativeBase):
    """Base model for database models"""


class DBManager:
    """Manage database engine and schema"""

    def __init__(self) -> None:
        self._engine: Engine | None = None

    def _connect_sqlite(self) -> None:
        """
        Connect to SQlite database
        """
        db_path = config.manager.config.database.path
        logger.info("Connecting to local sqlite database: %s", db_path)
        self._engine = create_engine(f"sqlite:///{db_path}")

    def init_db(self) -> None:
        """
        Initialise the database

        Will create any missing database schema objects (i.e. tables,
        relations). May be destructive based on previous database version.
        """

        logger.info("Initialising database. Creating missing objects")
        Base.metadata.create_all(self.engine)

    @property
    def engine(self) -> Engine:
        """
        The database engine

        If no engine currently exists, will fetch the configuration and
        connect to the configured database.

        Raises:
            UnsupportedDatabaseError: The database type specified in the
            configuration is not currently supported.

        Returns:
            Database engine
        """
        if self._engine is not None:
            return self._engine

        if config.manager.config.database.type == "sqlite":
            self._connect_sqlite()
        else:
            raise UnsupportedDatabaseError

        # We know _engine will be an Engine by this point
        return self._engine  # type: ignore

    def get_session(self):
        """
        Get a new session to the DB

        Yields:
            Created session
        """
        with Session(self.engine) as session:
            yield session

    def reset(self):
        """
        Reset the connection

        Will reset the connection and force a reconnect
        """
        self._engine = None


manager = DBManager()

DBSession = Annotated[Session, Depends(manager.get_session)]
