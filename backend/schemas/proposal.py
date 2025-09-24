from pydantic import BaseModel
from typing import Optional
from enum import Enum
from schemas.base import BaseResponseSchema

class ProposalStatus(str, Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    REPLIED = "Replied"
    WON = "Won"
    LOST = "Lost"

class ProposalCreate(BaseModel):
    opportunity_id: int
    content: str
    status: ProposalStatus = ProposalStatus.DRAFT

class ProposalUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[ProposalStatus] = None

class ProposalResponse(BaseResponseSchema):
    tenant_id: int
    opportunity_id: int
    content: str
    status: ProposalStatus