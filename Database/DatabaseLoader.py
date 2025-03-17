from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional, List, Type, TypeVar
from sqlalchemy.orm import selectinload

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
    from pydantic import BaseModel
################################################################################

__all__ = ("DatabaseLoader",)

T = TypeVar("T")

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
                selectinload(TopLevelDataModel.bg_checks).selectinload(BGCheckModel.venues),
                selectinload(TopLevelDataModel.profiles).selectinload(StaffProfileModel.additional_images),
                selectinload(TopLevelDataModel.profiles).selectinload(StaffProfileModel.availability),
                selectinload(TopLevelDataModel.temporary_jobs),
                selectinload(TopLevelDataModel.permanent_jobs),
            ).first()

            def map_schema(schema: Type[T], objects: List[Any]) -> List[T]:
                return [schema.model_validate(obj) for obj in objects]

            return MasterResponseSchema(
                channel_manager=ChannelManagerSchema.model_validate(top_level),
                role_manager=RoleManagerSchema.model_validate(top_level),
                venue_manager=VenueManagerSchema(
                    venues=[
                        VenueSchema.model_validate(
                            v,
                            context={"schedules": map_schema(VenueScheduleSchema, v.schedules)}
                        ) for v in top_level.venues
                    ]
                ),
                bg_check_manager=BGCheckManagerSchema(
                    bg_check_channel_id=top_level.bg_check_channel_id,
                    staff_role_id=top_level.staff_role_id,
                    staff_pending_role_id=top_level.staff_pending_role_id,
                    bg_checks=[
                        BGCheckSchema.model_validate(
                            bg,
                            context={"venues": map_schema(BGCheckVenueSchema, bg.venues)}
                        ) for bg in top_level.bg_checks
                    ]
                ),
                profile_manager=ProfileManagerSchema(
                    profiles=[
                        StaffProfileSchema.model_validate(
                            prof,
                            context={
                                "availability": map_schema(ProfileAvailabilitySchema, prof.availability),
                                "additional_images": map_schema(AdditionalImageSchema, prof.additional_images)
                            }
                        ) for prof in top_level.profiles
                    ]
                ),
                jobs_manager=JobsManagerSchema(
                    temporary_jobs=map_schema(TemporaryJobPostingSchema, top_level.temporary_jobs),
                    permanent_jobs=map_schema(PermanentJobPostingSchema, top_level.permanent_jobs),
                    trainee_message=TraineeMessageSchema(post_url=top_level.trainee_message_url),
                ),
            ).model_dump()

################################################################################
