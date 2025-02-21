from typing import Optional, List

from pydantic import BaseModel, RootModel

from .Venues import VenueManagerSchema
################################################################################

__all__ = (
    "GuildDataSchema",
    "TopLevelGuildSchema",
    "MasterResponseSchema",
    "LoggerConfigSchema",
)

################################################################################
class LoggerConfigSchema(BaseModel):

    log_channel_id: Optional[int]

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
    logger: LoggerConfigSchema
    venue_manager: VenueManagerSchema

    class Config:
        from_attributes = True

################################################################################
