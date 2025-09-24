from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List, Dict, Any
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

class LinkedInPostBatchCreate(BaseModel):
    posts: List[LinkedInPostCreate]

class PostIngestionResult(BaseModel):
    post_url: str
    status: str  # 'success', 'duplicate', 'failed'
    post_id: Optional[int] = None
    error: Optional[str] = None

class BatchIngestionResponse(BaseModel):
    total: int
    successful: int
    duplicates: int
    failed: int
    results: List[PostIngestionResult]