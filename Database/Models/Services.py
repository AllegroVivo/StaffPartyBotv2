from sqlalchemy import Column, Integer, BigInteger, ForeignKey, ARRAY, String, Boolean
from sqlalchemy.orm import relationship

from .Base import Base
################################################################################

__all__ = ("ServiceRequestModel",)

################################################################################
class ServiceRequestModel(Base):

    __tablename__ = "service_requests"

    top_level_id = Column(Integer, ForeignKey("top_level.id", name="temporary_jobs_top_level_fkey", ondelete="CASCADE"), nullable=False, server_default="1")
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    service = Column(Integer, nullable=False)
    dc = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    message_urls = Column(ARRAY(String), nullable=False, server_default="{}")
    accepted = Column(Boolean, nullable=False, server_default="false")
    post_url = Column(String, nullable=True)
    candidate_id = Column(BigInteger, nullable=True)

    # Relationships
    top_level = relationship("TopLevelDataModel", back_populates="service_requests")

################################################################################
