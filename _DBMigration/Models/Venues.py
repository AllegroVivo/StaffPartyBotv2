from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY, TIMESTAMP
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = (
    "VenueModel",
    "VenueScheduleModel",
    "SpecialEventModel",
)

################################################################################
class SpecialEventModel(Base):

    __tablename__ = "special_events"

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id", name="special_events_venues_fkey", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start = Column(String, nullable=True)
    length = Column(String, nullable=True)
    links = Column(ARRAY(String), nullable=False, server_default="{}")
    requirements = Column(String, nullable=True)
    post_url = Column(String, nullable=True)

    # Relationships
    venue = relationship("VenueModel", back_populates="special_events", passive_deletes=True)

################################################################################
class VenueScheduleModel(Base):

    __tablename__ = "venue_schedules"

    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id", name="venue_schedules_venues_fkey", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=True)
    start_hour = Column(Integer, nullable=True)
    start_minute = Column(Integer, nullable=True)
    end_hour = Column(Integer, nullable=True)
    end_minute = Column(Integer, nullable=True)
    interval_type = Column(Integer, nullable=True)
    interval_arg = Column(Integer, nullable=True)

    # Relationships
    venue = relationship("VenueModel", back_populates="schedules", passive_deletes=True)

################################################################################
class VenueModel(Base):

    __tablename__ = "venues"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="venues_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    xiv_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(ARRAY(String), nullable=False, server_default="{}")
    mare_id = Column(String, nullable=True)
    mare_password = Column(String, nullable=True)
    hiring = Column(Boolean, nullable=False, server_default="true")
    nsfw = Column(Boolean, nullable=False, server_default="false")
    data_center = Column(Integer, nullable=True)
    world = Column(Integer, nullable=True)
    zone = Column(Integer, nullable=True)
    ward = Column(Integer, nullable=True)
    plot = Column(Integer, nullable=True)
    subdivision = Column(Boolean, nullable=True)
    apartment = Column(Integer, nullable=True)
    room = Column(Integer, nullable=True)
    rp_level = Column(Integer, nullable=True)
    tags = Column(ARRAY(String), nullable=False, server_default="{}")
    user_ids = Column(ARRAY(BigInteger), nullable=False, server_default="{}")
    position_ids = Column(ARRAY(Integer), nullable=False, server_default="{}")
    mute_ids = Column(ARRAY(BigInteger), nullable=False, server_default="{}")
    discord_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    app_url = Column(String, nullable=True)
    post_url = Column(String, nullable=True)
    event_participation = Column(Boolean, nullable=False, server_default="false")

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="venues")
    schedules = relationship("VenueScheduleModel", back_populates="venue", passive_deletes=True)
    temporary_jobs = relationship("TemporaryJobPostingModel", back_populates="venue", passive_deletes=True)
    permanent_jobs = relationship("PermanentJobPostingModel", back_populates="venue", passive_deletes=True)
    special_events = relationship("SpecialEventModel", back_populates="venue", passive_deletes=True)

################################################################################
