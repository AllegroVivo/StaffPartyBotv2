from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "PermanentJobPostingSchema",
    "TemporaryJobPostingSchema",
    "JobsManagerSchema",
)

################################################################################
class PermanentJobPostingSchema(BaseModel):

    id: int

    class Config:
        from_attributes = True

################################################################################
class TemporaryJobPostingSchema(BaseModel):

    id: int
    venue_id: int
    user_id: int
    position_id: int
    description: Optional[str]
    salary: Optional[str]
    start_dt: Optional[datetime]
    end_dt: Optional[datetime]
    candidate_id: Optional[int]
    post_url: Optional[str]

    class Config:
        from_attributes = True

################################################################################
class JobsManagerSchema(BaseModel):

    temporary_jobs: List[TemporaryJobPostingSchema]
    permanent_jobs: List[PermanentJobPostingSchema]

    class Config:
        from_attributes = True

################################################################################
