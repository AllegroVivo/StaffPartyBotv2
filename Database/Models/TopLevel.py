from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("GuildIDModel", "TopLevelDataModel")

################################################################################
class GuildIDModel(Base):

    __tablename__ = "guild_ids"

    id = Column(BigInteger, primary_key=True)

    # Relationships

################################################################################
class TopLevelDataModel(Base):

    __tablename__ = "top_level"

    id = Column(Integer, primary_key=True)
    venue_channel_id = Column(BigInteger, nullable=True)

    # Relationships
    config = relationship("TopLevelConfigModel", back_populates="master", passive_deletes=True)

################################################################################
