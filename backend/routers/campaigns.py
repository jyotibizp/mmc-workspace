from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.campaign_controller import CampaignController
from schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
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