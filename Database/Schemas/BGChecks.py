from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "BGCheckVenueSchema",
    "BGCheckSchema",
    "BGCheckManagerSchema",
)

################################################################################
class BGCheckVenueSchema(BaseModel):

    id: int
    name: str
    data_center: int
    world: int
    jobs: List[str]

    class Config:
        from_attributes = True

################################################################################
class BGCheckSchema(BaseModel):

    id: int
    agree: bool
    names: List[str] = []
    user_id: int
    approved: bool
    post_url: Optional[str]
    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    approved_by: Optional[int]
    venues: List[BGCheckVenueSchema] = []

    class Config:
        from_attributes = True

################################################################################
class BGCheckManagerSchema(BaseModel):

    bg_check_channel_id: Optional[int]
    staff_role_id: Optional[int]
    staff_pending_role_id: Optional[int]
    bg_checks: List[BGCheckSchema]

    class Config:
        from_attributes = True

################################################################################
