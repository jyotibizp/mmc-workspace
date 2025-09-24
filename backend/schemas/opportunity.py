from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from schemas.base import BaseResponseSchema

class OpportunityStatus(str, Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    REPLIED = "Replied"
    WON = "Won"
    LOST = "Lost"

class OpportunityCreate(BaseModel):
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    source_post_id: Optional[int] = None
    title: str
    summary: Optional[str] = None
    status: OpportunityStatus = OpportunityStatus.DRAFT
    tags: List[str] = []

class OpportunityUpdate(BaseModel):
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[OpportunityStatus] = None
    tags: Optional[List[str]] = None

class OpportunityResponse(BaseResponseSchema):
    tenant_id: int
    company_id: Optional[int]
    contact_id: Optional[int]
    source_post_id: Optional[int]
    title: str
    summary: Optional[str]
    status: OpportunityStatus
    tags: List[str]