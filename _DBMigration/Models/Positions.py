from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, String, ARRAY
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("RequirementModel", "PositionModel")

################################################################################
class RequirementModel(Base):

    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True)
    position_id = Column(Integer, ForeignKey("positions.id", name="positions_requirements_fkey", ondelete="CASCADE"), nullable=True)
    text = Column(String, nullable=False)

    # Relationships
    position = relationship("PositionModel", back_populates="requirements")

################################################################################
class PositionModel(Base):

    __tablename__ = "positions"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="positions_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    role_id = Column(BigInteger, nullable=True)
    description = Column(String, nullable=True)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="positions")
    requirements = relationship("RequirementModel", back_populates="position", passive_deletes=True)
    temporary_jobs = relationship("TemporaryJobPostingModel", back_populates="position", passive_deletes=True)

################################################################################
