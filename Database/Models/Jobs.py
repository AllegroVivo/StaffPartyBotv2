from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("PermanentJobPostingModel", "TemporaryJobPostingModel")

################################################################################
class PermanentJobPostingModel(Base):

    __tablename__ = "permanent_jobs"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="permanent_jobs_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id", name="temporary_jobs_venues_fkey", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    description = Column(String, nullable=False)
    position_id = Column(Integer, nullable=False)
    post_url = Column(String, nullable=True)
    salary = Column(String, nullable=True)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="permanent_jobs")
    venue = relationship("VenueModel", back_populates="permanent_jobs")

################################################################################
class TemporaryJobPostingModel(Base):

    __tablename__ = "temporary_jobs"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="temporary_jobs_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("venues.id", name="temporary_jobs_venues_fkey", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    candidate_id = Column(BigInteger, nullable=True)
    description = Column(String, nullable=False)
    position_id = Column(Integer, nullable=False)
    post_url = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    start_dt = Column(TIMESTAMP, nullable=False)
    end_dt = Column(TIMESTAMP, nullable=False)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="temporary_jobs")
    venue = relationship("VenueModel", back_populates="temporary_jobs")

################################################################################
