from typing import Optional, List

from pydantic import BaseModel

from .BGChecks import BGCheckManagerSchema
from .Jobs import JobsManagerSchema
from .Profiles import ProfileManagerSchema
from .Venues import VenueManagerSchema
################################################################################

__all__ = (
    "GuildDataSchema",
    "TopLevelGuildSchema",
    "MasterResponseSchema",
    "ChannelManagerSchema",
    "RoleManagerSchema",
)

################################################################################
class RoleManagerSchema(BaseModel):

    staff_role_id: Optional[int]
    staff_pending_role_id: Optional[int]
    venue_management_role_id: Optional[int]
    trainee_role_id: Optional[int]
    trainee_hiatus_role_id: Optional[int]

    class Config:
        from_attributes = True

################################################################################
class ChannelManagerSchema(BaseModel):

    log_channel_id: Optional[int]
    venue_channel_id: Optional[int]
    temp_job_channel_id: Optional[int]
    perm_jobs_channel_id: Optional[int]
    profile_channel_id: Optional[int]
    welcome_channel_id: Optional[int]
    group_training_channel_id: Optional[int]
    bg_check_channel_id: Optional[int]

    class Config:
        from_attributes = True

################################################################################
class GuildDataSchema(BaseModel):

    class Config:
        from_attributes = True

################################################################################
class TopLevelGuildSchema(BaseModel):

    id: int
    data: GuildDataSchema

    class Config:
        from_attributes = True

################################################################################
class MasterResponseSchema(BaseModel):

    # guilds: List[TopLevelGuildSchema]
    channel_manager: ChannelManagerSchema
    role_manager: RoleManagerSchema
    venue_manager: VenueManagerSchema
    bg_check_manager: BGCheckManagerSchema
    profile_manager: ProfileManagerSchema
    jobs_manager: JobsManagerSchema

    class Config:
        from_attributes = True

################################################################################
