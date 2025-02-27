from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "AdditionalImageSchema",
    "StaffProfileSchema",
    "ProfileManagerSchema",
)

################################################################################
class AdditionalImageSchema(BaseModel):

    id: int
    url: str
    caption: Optional[str]

    class Config:
        from_attributes = True

################################################################################
class StaffProfileSchema(BaseModel):

    user_id: int
    post_url: Optional[str]
    # Details
    name: Optional[str]
    url: Optional[str]
    color: Optional[int]
    jobs: List[str] = []
    rates: Optional[str]
    position_ids: List[int]
    dm_pref: bool
    timezone: Optional[int]
    # At A Glance
    gender: Optional[str]
    pronouns: List[int]
    race: Optional[str]
    clan: Optional[str]
    orientation: Optional[str]
    height: Optional[int]
    age: Optional[str]
    mare: Optional[str]
    data_centers: List[int]
    # Personality
    likes: List[str]
    dislikes: List[str]
    personality: Optional[str]
    about_me: Optional[str]
    # Images
    thumbnail_url: Optional[str]
    main_image_url: Optional[str]
    additional_images: List[AdditionalImageSchema] = []

    class Config:
        from_attributes = True

################################################################################
class ProfileManagerSchema(BaseModel):

    profiles: List[StaffProfileSchema]

    class Config:
        from_attributes = True

################################################################################
