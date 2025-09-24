from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalyzeExtractRequest(BaseModel):
    post_id: int

class AnalyzeExtractResponse(BaseModel):
    opportunity_detected: bool
    company_info: Optional[Dict[str, Any]] = None
    contact_info: Optional[Dict[str, Any]] = None
    opportunity_details: Optional[Dict[str, Any]] = None
    urgency: Optional[str] = None
    classification: Optional[List[str]] = None
    confidence_score: Optional[float] = None

class ProposalGenerationRequest(BaseModel):
    opportunity_id: int
    template_id: Optional[int] = None
    additional_context: Optional[str] = None

class ProposalGenerationResponse(BaseModel):
    proposal_content: str
    suggested_sections: List[Dict[str, str]]