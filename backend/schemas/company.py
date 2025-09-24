from pydantic import BaseModel, HttpUrl
from typing import Optional
from schemas.base import BaseResponseSchema

class CompanyCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

class CompanyResponse(BaseResponseSchema):
    tenant_id: int
    name: str
    domain: Optional[str]
    linkedin_url: Optional[str]