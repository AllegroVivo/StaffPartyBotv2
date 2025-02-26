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
    def venue_schedule(self, venue_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_schedule = VenueScheduleModel(venue_id=venue_id)
                db.add(new_schedule)
                db.commit()
                db.refresh(new_schedule)
                return VenueScheduleSchema.model_validate(new_schedule).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating venue schedule: {str(e)}")

################################################################################
    def position(self, pos_name: str) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_pos = PositionModel(name=pos_name)
                db.add(new_pos)
                db.commit()
                db.refresh(new_pos)
                return PositionSchema.model_validate(new_pos).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating position: {str(e)}")

################################################################################
    def requirement(self, pos_id: Optional[int], text: str) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_req = RequirementModel(position_id=pos_id, text=text)
                db.add(new_req)
                db.commit()
                db.refresh(new_req)
                return RequirementSchema.model_validate(new_req).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating requirement: {str(e)}")

################################################################################
    def bg_check(self, user_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_bg = BGCheckModel(user_id=user_id)
                db.add(new_bg)
                db.commit()
                db.refresh(new_bg)
                return BGCheckSchema.model_validate(new_bg).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating background check: {str(e)}")

################################################################################
    def bg_check_venue(self, parent_id: int, name: str, data_center: int, world: int, jobs: List[str]):

        with self._parent._get_db() as db:
            try:
                new_bg_venue = BGCheckVenueModel(
                    bg_check_id=parent_id,
                    name=name,
                    data_center=data_center,
                    world=world,
                    jobs=jobs
                )
                db.add(new_bg_venue)
                db.commit()
                db.refresh(new_bg_venue)
                return BGCheckVenueSchema.model_validate(new_bg_venue).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating background check venue: {str(e)}")

################################################################################
