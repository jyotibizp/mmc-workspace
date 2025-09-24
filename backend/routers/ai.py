from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.ai_controller import AIController
from schemas.ai import AnalyzeExtractRequest, ProposalGenerationRequest

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