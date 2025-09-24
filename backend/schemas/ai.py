from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Legacy schemas (to be deprecated)
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

# New unified AI endpoint schemas
class AnalyzeOpportunityRequest(BaseModel):
    post_id: int
    enable_cache: bool = True

class CompanySuggestion(BaseModel):
    name: str
    confidence: float
    domain: Optional[str] = None
    linkedin_url: Optional[str] = None

class ContactSuggestion(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    confidence: float = 0.0

class ExtractedField(BaseModel):
    value: Any
    confidence: float

class AnalyzeOpportunityResponse(BaseModel):
    is_opportunity: bool
    confidence: float
    extracted_fields: Dict[str, ExtractedField]
    company_suggestion: Optional[CompanySuggestion] = None
    contact_suggestion: Optional[ContactSuggestion] = None
    category: str
    urgency: str
    tags: List[str]
    budget_range: Optional[str] = None
    timeline: Optional[str] = None

class ProposalGenerationRequest(BaseModel):
    opportunity_id: int
    template_id: Optional[int] = None
    additional_context: Optional[str] = None

class ProposalGenerationResponse(BaseModel):
    proposal_content: str
    suggested_sections: List[Dict[str, str]]