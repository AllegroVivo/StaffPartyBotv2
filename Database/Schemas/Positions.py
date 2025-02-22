from typing import Optional, List

from pydantic import BaseModel, RootModel

from .Venues import VenueManagerSchema
################################################################################

__all__ = (
    "RequirementSchema",
    "PositionSchema",
    "PositionManagerSchema",
)

################################################################################
class RequirementSchema(BaseModel):

    id: int
    position_id: int

    class Config:
        from_attributes = True

################################################################################
class PositionSchema(BaseModel):

    id: int
    name: str
    requirement_ids: List[int]
    role_id: Optional[int]
    description: Optional[str]

    class Config:
        from_attributes = True

################################################################################
class PositionManagerSchema(BaseModel):

    positions: List[PositionSchema]
    global_requirements: List[RequirementSchema]

    class Config:
        from_attributes = True

################################################################################
