from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from .DatabaseDeleter import DatabaseDeleter
from .DatabaseInserter import DatabaseInserter
from .DatabaseLoader import DatabaseLoader
from .DatabaseUpdater import DatabaseUpdater

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("Database", )

################################################################################
class Database:

    __slots__ = (
        "_state",
        "_inserter",
        "_updater",
        "_deleter",
        "_loader",
        "_engine",
        "_session",
    )

################################################################################
    def __init__(self, state: StaffPartyBot) -> None:

        self._state: StaffPartyBot = state

        load_dotenv()
        self._engine: Engine = create_engine(
            os.getenv("DEVELOPMENT_DATABASE_URL")
            if os.getenv("DEBUG") == "True"
            else os.getenv("DATABASE_URL"),
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
            pool_timeout=30,
            pool_recycle=1800
        )
        self._session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        )

        self._inserter: DatabaseInserter = DatabaseInserter(self)
        self._updater: DatabaseUpdater = DatabaseUpdater(self)
        self._deleter: DatabaseDeleter = DatabaseDeleter(self)
        self._loader: DatabaseLoader = DatabaseLoader(self)

################################################################################
    @property
    def insert(self) -> DatabaseInserter:

        return self._inserter

################################################################################
    @property
    def update(self) -> DatabaseUpdater:

        return self._updater

################################################################################
    @property
    def delete(self) -> DatabaseDeleter:

        return self._deleter

################################################################################
    @contextmanager
    def _get_db(self) -> Session:

        db = self._session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

################################################################################
    def load_all(self) -> Optional[Dict[str, Any]]:

        return self._loader.load_all()

################################################################################
    def fetch_guild(self, guild_id: int) -> bool:

        return self._loader.check_guild(guild_id)

################################################################################
