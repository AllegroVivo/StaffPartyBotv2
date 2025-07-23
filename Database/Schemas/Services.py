from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "ServiceRequestManagerSchema",
    "ServiceRequestSchema"
)

################################################################################
class ServiceRequestSchema(BaseModel):

    id: int
    user_id: int
    service: Optional[int]
    description: Optional[str]
    dc: Optional[int]
    budget: Optional[str]
    message_urls: List[str]
    accepted: bool
    post_url: Optional[str]
    candidate_id: Optional[int]

    class Config:
        from_attributes = True

################################################################################
class ServiceRequestManagerSchema(BaseModel):

    service_requests: List[ServiceRequestSchema]

    class Config:
        from_attributes = True

################################################################################
