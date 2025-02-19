from typing import Optional, List

from pydantic import BaseModel, RootModel
################################################################################

__all__ = (
    "GuildDataSchema",
    "TopLevelGuildSchema",
    "MasterResponseSchema",
)

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
class MasterResponseSchema(RootModel):

    root: List[TopLevelGuildSchema]

    class Config:
        from_attributes = True

################################################################################
