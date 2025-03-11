from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, ARRAY
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

    # Channels
    venue_channel_id = Column(BigInteger, nullable=True)
    log_channel_id = Column(BigInteger, nullable=True)
    temp_job_channel_id = Column(BigInteger, nullable=True)
    perm_jobs_channel_id = Column(BigInteger, nullable=True)
    profile_channel_id = Column(BigInteger, nullable=True)
    welcome_channel_id = Column(BigInteger, nullable=True)
    group_training_channel_id = Column(BigInteger, nullable=True)
    bg_check_channel_id = Column(BigInteger, nullable=True)
    restart_channel_ids = Column(ARRAY(BigInteger), nullable=True)

    # Roles
    staff_role_id = Column(BigInteger, nullable=True)
    staff_pending_role_id = Column(BigInteger, nullable=True)
    venue_management_role_id = Column(BigInteger, nullable=True)
    trainee_role_id = Column(BigInteger, nullable=True)
    trainee_hiatus_role_id = Column(BigInteger, nullable=True)

    # Relationships
    venues = relationship("VenueModel", back_populates="top_level", passive_deletes=True)
    positions = relationship("PositionModel", back_populates="top_level", passive_deletes=True)
    bg_checks = relationship("BGCheckModel", back_populates="top_level", passive_deletes=True)
    profiles = relationship("StaffProfileModel", back_populates="top_level", passive_deletes=True)
    temporary_jobs = relationship("TemporaryJobPostingModel", back_populates="top_level", passive_deletes=True)
    permanent_jobs = relationship("PermanentJobPostingModel", back_populates="top_level", passive_deletes=True)

################################################################################
