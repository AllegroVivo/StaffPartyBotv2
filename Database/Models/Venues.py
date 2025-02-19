from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = (
    "VenueModel",
    "VenueScheduleModel",
)

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

    id = Column(Integer, primary_key=True)
    xiv_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(ARRAY(String), nullable=False, server_default="{}")
    mare_id = Column(String, nullable=True)
    mare_password = Column(String, nullable=True)
    hiring = Column(Boolean, nullable=False, server_default="true")
    pending = Column(Boolean, nullable=False, server_default="true")
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

    # Relationships
    schedules = relationship("VenueScheduleModel", back_populates="venue", passive_deletes=True)

################################################################################
