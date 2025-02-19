from __future__ import annotations

import re
from typing import TYPE_CHECKING, List, Optional, Any, Dict
from uuid import uuid4

from discord import Guild
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseInserter", )

################################################################################
class DatabaseInserter:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def guild(self, guild: Guild) -> None:

        with self._parent._get_db() as db:
            gid = guild.id
            query = db.query(GuildIDModel).filter(GuildIDModel.id == gid)
            existing = query.first()

            if existing is not None:
                raise ValueError(f"Guild {gid} already exists in the database.")

            try:
                new_guild = GuildIDModel(id=gid)
                db.add(new_guild)
                db.commit()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating guild: {str(e)}")

################################################################################
    def venue(self, xiv_id: str, name: str) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            query = db.query(VenueModel).filter(VenueModel.xiv_id == xiv_id)
            existing = query.first()

            if existing is not None:
                raise ValueError(f"Venue with XIV ID '{xiv_id}' already exists in the database.")

            try:
                new_venue = VenueModel(xiv_id=xiv_id, name=name)
                db.add(new_venue)
                db.commit()
                db.refresh(new_venue)
                return VenueSchema.model_validate(new_venue).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating venue: {str(e)}")

################################################################################
