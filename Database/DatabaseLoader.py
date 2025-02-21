from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict, Any, Optional
from sqlalchemy.orm import selectinload

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def check_guild(self, guild_id: int) -> bool:

        with self._parent._get_db() as db:
            try:
                guild = db.query(GuildIDModel).filter(GuildIDModel.id == guild_id).first()
            except Exception as e:
                print(e)
                return False

            return guild is not None

################################################################################
    def load_all(self) -> Optional[Dict[str, Any]]:

        with self._parent._get_db() as db:
            top_level = db.query(TopLevelDataModel).options(
                selectinload(TopLevelDataModel.venues).selectinload(VenueModel.schedules),
            ).first()

            return MasterResponseSchema(
                logger=LoggerConfigSchema(log_channel_id=top_level.log_channel_id),
                venue_manager=VenueManagerSchema(
                    post_channel_id=top_level.venue_channel_id,
                    venues=[
                        VenueSchema(
                            id=v.id,
                            xiv_id=v.xiv_id,
                            name=v.name,
                            description=v.description,
                            mare_id=v.mare_id,
                            mare_password=v.mare_password,
                            hiring=v.hiring,
                            nsfw=v.nsfw,
                            data_center=v.data_center,
                            world=v.world,
                            zone=v.zone,
                            ward=v.ward,
                            plot=v.plot,
                            subdivision=v.subdivision,
                            apartment=v.apartment,
                            room=v.room,
                            rp_level=v.rp_level,
                            tags=v.tags,
                            user_ids=v.user_ids,
                            position_ids=v.position_ids,
                            mute_ids=v.mute_ids,
                            discord_url=v.discord_url,
                            website_url=v.website_url,
                            banner_url=v.banner_url,
                            logo_url=v.logo_url,
                            app_url=v.app_url,
                            post_url=v.post_url,
                            schedules=[VenueScheduleSchema.model_validate(sch) for sch in v.schedules]
                        ) for v in top_level.venues
                    ]
                )
            ).model_dump()

################################################################################
