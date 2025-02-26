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
                selectinload(TopLevelDataModel.positions).selectinload(PositionModel.requirements),
                selectinload(TopLevelDataModel.bg_checks).selectinload(BGCheckModel.venues),
            ).first()
            global_reqs = db.query(RequirementModel).filter_by(position_id=None).all()

            return MasterResponseSchema(
                channel_manager=ChannelManagerSchema.model_validate(top_level),
                role_manager=RoleManagerSchema.model_validate(top_level),
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
                ),
                position_manager=PositionManagerSchema(
                    global_requirements=[RequirementSchema.model_validate(req) for req in global_reqs],
                    positions=[
                        PositionSchema(
                            id=p.id,
                            name=p.name,
                            description=p.description,
                            role_id=p.role_id,
                            requirements=[RequirementSchema.model_validate(req) for req in p.requirements],
                        ) for p in top_level.positions
                    ]
                ),
                bg_check_manager=BGCheckManagerSchema(
                    bg_check_channel_id=top_level.bg_check_channel_id,
                    staff_role_id=top_level.staff_role_id,
                    staff_pending_role_id=top_level.staff_pending_role_id,
                    bg_checks=[
                        BGCheckSchema(
                            id=bg.id,
                            agree=bg.agree,
                            names=bg.names,
                            user_id=bg.user_id,
                            approved=bg.approved,
                            post_url=bg.post_url,
                            submitted_at=bg.submitted_at,
                            approved_at=bg.approved_at,
                            approved_by=bg.approved_by,
                            venues=[BGCheckVenueSchema.model_validate(v) for v in bg.venues],
                        ) for bg in top_level.bg_checks
                    ]
                )
            ).model_dump()

################################################################################
