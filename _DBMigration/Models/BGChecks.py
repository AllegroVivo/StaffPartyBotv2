from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY, TIMESTAMP
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("BGCheckVenueModel", "BGCheckModel")

################################################################################
class BGCheckVenueModel(Base):

    __tablename__ = "bg_check_venues"

    id = Column(Integer, primary_key=True)
    bg_check_id = Column(Integer, ForeignKey("bg_checks.id", name="bg_check_venues_bg_checks_fkey", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    data_center = Column(Integer, nullable=False)
    world = Column(Integer, nullable=False)
    jobs = Column(ARRAY(String), nullable=False)

    # Relationships
    bg_check = relationship("BGCheckModel", back_populates="venues", passive_deletes=True)

################################################################################
class BGCheckModel(Base):

    __tablename__ = "bg_checks"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="bg_checks_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    agree = Column(Boolean, nullable=False, server_default="false")
    names = Column(ARRAY(String), nullable=False, server_default="{}")
    approved = Column(Boolean, nullable=False, server_default="false")
    post_url = Column(String, nullable=True)
    submitted_at = Column(TIMESTAMP(), nullable=True)
    approved_at = Column(TIMESTAMP(), nullable=True)
    approved_by = Column(BigInteger, nullable=True)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="bg_checks", passive_deletes=True)
    venues = relationship("BGCheckVenueModel", back_populates="bg_check", passive_deletes=True)

################################################################################
