from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.base import BaseResponseSchema

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CampaignResponse(BaseResponseSchema):
    tenant_id: int
    name: str
    description: Optional[str]

class CampaignNoteCreate(BaseModel):
    campaign_id: int
    opportunity_id: int
    note: str
    follow_up_at: Optional[datetime] = None

class CampaignNoteUpdate(BaseModel):
    note: Optional[str] = None
    follow_up_at: Optional[datetime] = None
    completed: Optional[bool] = None

class CampaignNoteResponse(BaseResponseSchema):
    tenant_id: int
    campaign_id: int
    opportunity_id: int
    note: str
    follow_up_at: Optional[datetime]
    completed: bool