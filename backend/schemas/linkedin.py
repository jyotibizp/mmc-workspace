from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from schemas.base import BaseResponseSchema

class LinkedInPostCreate(BaseModel):
    post_url: HttpUrl
    author_profile_url: Optional[HttpUrl] = None
    content: str
    scraped_at: datetime

class LinkedInPostResponse(BaseResponseSchema):
    tenant_id: int
    user_id: Optional[int]
    post_url: str
    author_profile_url: Optional[str]
    content: str
    scraped_at: datetime