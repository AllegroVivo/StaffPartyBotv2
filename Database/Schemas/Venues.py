from typing import Optional, List

from pydantic import BaseModel, RootModel
################################################################################

__all__ = (
    "VenueManagerSchema",
    "VenueSchema",
    "VenueScheduleSchema",
)

################################################################################
class VenueScheduleSchema(BaseModel):

    id: int
    day: Optional[int]
    start_hour: Optional[int]
    start_minute: Optional[int]
    end_hour: Optional[int]
    end_minute: Optional[int]
    interval_type: Optional[int]
    interval_arg: Optional[int]

    class Config:
        from_attributes = True

################################################################################
class VenueSchema(BaseModel):

    id: int
    xiv_id: str
    name: str
    description: List[str]
    mare_id: Optional[str]
    mare_password: Optional[str]
    hiring: bool
    nsfw: bool
    data_center: Optional[int]
    world: Optional[int]
    zone: Optional[int]
    ward: Optional[int]
    plot: Optional[int]
    subdivision: Optional[int]
    apartment: Optional[int]
    room: Optional[int]
    rp_level: Optional[int]
    tags: List[str]
    user_ids: List[int]
    position_ids: List[int]
    mute_ids: List[int]
    discord_url: Optional[str]
    website_url: Optional[str]
    banner_url: Optional[str]
    logo_url: Optional[str]
    app_url: Optional[str]
    post_url: Optional[str]
    schedules: List[VenueScheduleSchema] = []

    class Config:
        from_attributes = True

################################################################################
class VenueManagerSchema(BaseModel):

    venues: List[VenueSchema]

    class Config:
        from_attributes = True

################################################################################
