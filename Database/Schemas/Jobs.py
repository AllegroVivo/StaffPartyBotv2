from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "PermanentJobPostingSchema",
    "TemporaryJobPostingSchema",
    "JobsManagerSchema",
    "TraineeMessageSchema",
)

################################################################################
class TraineeMessageSchema(BaseModel):

    post_url: Optional[str]

    class Config:
        from_attributes = True

################################################################################
class PermanentJobPostingSchema(BaseModel):

    id: int
    venue_id: int
    user_id: int
    description: str
    position_id: int
    post_url: Optional[str]
    salary: Optional[str]
    candidate_id: Optional[int]

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
    genres: List[int] = []

    class Config:
        from_attributes = True

################################################################################
class JobsManagerSchema(BaseModel):

    temporary_jobs: List[TemporaryJobPostingSchema]
    permanent_jobs: List[PermanentJobPostingSchema]
    trainee_message: TraineeMessageSchema

    class Config:
        from_attributes = True

################################################################################
