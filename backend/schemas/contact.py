from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from schemas.base import BaseResponseSchema

class ContactCreate(BaseModel):
    company_id: Optional[int] = None
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_profile_url: Optional[HttpUrl] = None

class ContactUpdate(BaseModel):
    company_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_profile_url: Optional[HttpUrl] = None

class ContactResponse(BaseResponseSchema):
    tenant_id: int
    company_id: Optional[int]
    name: str
    email: Optional[str]
    phone: Optional[str]
    linkedin_profile_url: Optional[str]