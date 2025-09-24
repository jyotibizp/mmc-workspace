from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.campaign_controller import CampaignController
from schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignNoteCreate, CampaignNoteUpdate, CampaignNoteResponse
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.create_campaign(campaign, tenant_id)

@router.get("/", response_model=List[CampaignResponse])
async def get_campaigns(
    tenant_id: int = Depends(get_current_tenant_id),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.get_campaigns(tenant_id, skip, limit, search)

@router.get("/statistics")
async def get_campaign_statistics(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.get_campaign_statistics(tenant_id)

@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.get_campaign(campaign_id, tenant_id)

@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.update_campaign(campaign_id, campaign_update, tenant_id)

@router.post("/{campaign_id}/archive", response_model=CampaignResponse)
async def archive_campaign(
    campaign_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.archive_campaign(campaign_id, tenant_id)

@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.delete_campaign(campaign_id, tenant_id)

# Campaign Notes endpoints
@router.post("/notes", response_model=CampaignNoteResponse)
async def create_campaign_note(
    note: CampaignNoteCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.create_campaign_note(note, tenant_id)

@router.get("/{campaign_id}/notes", response_model=List[CampaignNoteResponse])
async def get_campaign_notes(
    campaign_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get all notes for a specific campaign."""
    controller = CampaignController(db)
    return controller.get_campaign_notes(campaign_id, tenant_id)

@router.get("/notes/{note_id}", response_model=CampaignNoteResponse)
async def get_campaign_note(
    note_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.get_campaign_note(note_id, tenant_id)

@router.put("/notes/{note_id}", response_model=CampaignNoteResponse)
async def update_campaign_note(
    note_id: int,
    note_update: CampaignNoteUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.update_campaign_note(note_id, note_update, tenant_id)

@router.delete("/notes/{note_id}")
async def delete_campaign_note(
    note_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CampaignController(db)
    return controller.delete_campaign_note(note_id, tenant_id)

@router.get("/follow-ups/overdue", response_model=List[CampaignNoteResponse])
async def get_overdue_follow_ups(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get overdue follow-up notes for the tenant."""
    controller = CampaignController(db)
    return controller.get_overdue_follow_ups(tenant_id)

@router.get("/notes/by-opportunity/{opportunity_id}", response_model=List[CampaignNoteResponse])
async def get_notes_by_opportunity(
    opportunity_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get all notes for a specific opportunity across campaigns."""
    controller = CampaignController(db)
    return controller.get_notes_by_opportunity(opportunity_id, tenant_id)