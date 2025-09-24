from pydantic import BaseModel
from typing import Optional
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