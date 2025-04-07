from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "DJManagerSchema",
    "DJProfileSchema",
    "DJAvailabilitySchema",
)

################################################################################
class DJAvailabilitySchema(BaseModel):

    id: int
    day: int
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int

    class Config:
        from_attributes = True

################################################################################
class DJProfileSchema(BaseModel):

    user_id: int
    color: Optional[int]
    name: Optional[str]
    nsfw: bool
    genres: List[int] = []
    aboutme: Optional[str]
    rates: Optional[str]
    logo_url: Optional[str]
    image_url: Optional[str]
    dm_pref: bool
    post_url: Optional[str]
    regions: List[int] = []
    links: List[str] = []
    availability: List[DJAvailabilitySchema] = []
    muted_venue_ids: List[int] = []

    class Config:
        from_attributes = True

################################################################################
class DJManagerSchema(BaseModel):

    profiles: List[DJProfileSchema]

    class Config:
        from_attributes = True

################################################################################
