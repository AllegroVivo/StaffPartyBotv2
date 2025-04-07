from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("DJProfileModel", "DJProfileAvailabilityModel")

################################################################################
class DJProfileAvailabilityModel(Base):

    __tablename__ = "dj_profile_availabilities"

    id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, ForeignKey("dj_profiles.user_id", name="dj_profile_availability_dj_profiles_fkey", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=False)
    start_hour = Column(Integer, nullable=False)
    start_minute = Column(Integer, nullable=False)
    end_hour = Column(Integer, nullable=False)
    end_minute = Column(Integer, nullable=False)

    # Relationships
    profile = relationship("DJProfileModel", back_populates="availability", passive_deletes=True)

################################################################################
class DJProfileModel(Base):

    __tablename__ = "dj_profiles"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="dj_profiles_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    user_id = Column(BigInteger, primary_key=True)
    color = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    nsfw = Column(Boolean, nullable=False, server_default="false")
    genres = Column(ARRAY(Integer), nullable=False, server_default="{}")
    aboutme = Column(String, nullable=True)
    rates = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    links = Column(ARRAY(String), nullable=False, server_default="{}")
    dm_pref = Column(Boolean, nullable=False, server_default="true")
    post_url = Column(String, nullable=True)
    regions = Column(ARRAY(Integer), nullable=False, server_default="{}")
    muted_venue_ids = Column(ARRAY(BigInteger), nullable=False, server_default="{}")

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="dj_profiles")
    availability = relationship("DJProfileAvailabilityModel", back_populates="profile", passive_deletes=True)

################################################################################
