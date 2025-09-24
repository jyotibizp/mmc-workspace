from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.ai_controller import AIController
from schemas.ai import AnalyzeExtractRequest, ProposalGenerationRequest, AnalyzeOpportunityRequest, AnalyzeOpportunityResponse

router = APIRouter()

@router.post("/analyze-extract")
async def analyze_extract_post(
    request: AnalyzeExtractRequest,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = AIController(db)
    return await controller.analyze_extract_post(request, tenant_id)

@router.post("/generate-proposal")
async def generate_proposal(
    request: ProposalGenerationRequest,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = AIController(db)
    return await controller.generate_proposal(request, tenant_id)

@router.post("/analyze-opportunity", response_model=AnalyzeOpportunityResponse)
async def analyze_opportunity(
    request: AnalyzeOpportunityRequest,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Unified AI analysis endpoint. Loads post context server-side and performs
    comprehensive opportunity analysis including company/contact detection.
    """
    controller = AIController(db)
    return await controller.analyze_opportunity(request, tenant_id)

@router.post("/analyze-opportunity/stream")
async def analyze_opportunity_streaming(
    request: AnalyzeOpportunityRequest,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """
    Streaming version of AI analysis endpoint. Returns progressive updates
    during the analysis process via Server-Sent Events.
    """
    controller = AIController(db)
    return await controller.analyze_opportunity_streaming(request, tenant_id)