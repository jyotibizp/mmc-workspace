from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.proposal_controller import ProposalController
from schemas.proposal import ProposalCreate, ProposalUpdate, ProposalResponse
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=ProposalResponse)
async def create_proposal(
    proposal: ProposalCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.create_proposal(proposal, tenant_id)

@router.post("/generate-ai", response_model=dict)
async def generate_proposal_with_ai(
    opportunity_id: int = Query(..., description="Opportunity ID to generate proposal for"),
    additional_context: Optional[str] = Query(None, description="Additional context for AI generation"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return await controller.generate_proposal_with_ai(opportunity_id, tenant_id, additional_context)

@router.get("/", response_model=List[ProposalResponse])
async def get_proposals(
    tenant_id: int = Depends(get_current_tenant_id),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.get_proposals(tenant_id, skip, limit, status, search)

@router.get("/statistics")
async def get_proposal_statistics(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.get_proposal_statistics(tenant_id)

@router.get("/by-opportunity/{opportunity_id}", response_model=Optional[ProposalResponse])
async def get_proposal_by_opportunity(
    opportunity_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.get_proposal_by_opportunity(opportunity_id, tenant_id)

@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.get_proposal(proposal_id, tenant_id)

@router.get("/{proposal_id}/export")
async def export_proposal(
    proposal_id: int,
    format: str = Query("markdown", description="Export format: markdown, html, text"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.export_proposal(proposal_id, tenant_id, format)

@router.post("/{proposal_id}/duplicate", response_model=ProposalResponse)
async def duplicate_proposal(
    proposal_id: int,
    new_opportunity_id: int = Query(..., description="Opportunity ID for the duplicated proposal"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.duplicate_proposal(proposal_id, new_opportunity_id, tenant_id)

@router.put("/{proposal_id}", response_model=ProposalResponse)
async def update_proposal(
    proposal_id: int,
    proposal_update: ProposalUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.update_proposal(proposal_id, proposal_update, tenant_id)

@router.delete("/{proposal_id}")
async def delete_proposal(
    proposal_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ProposalController(db)
    return controller.delete_proposal(proposal_id, tenant_id)