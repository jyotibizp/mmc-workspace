from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.base import BaseResponseSchema

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    size: int
    url: str
    proposal_id: int
    created_at: str

class ProposalFileResponse(BaseResponseSchema):
    tenant_id: int
    proposal_id: int
    filename: str
    size: int
    url: str

class FileStatisticsResponse(BaseModel):
    total_files: int
    total_storage_bytes: int
    total_storage_mb: float
    storage_limit_mb: float
    files_limit: int
    storage_usage_percent: float

class FileCleanupResponse(BaseModel):
    cleaned_files: int
    message: str