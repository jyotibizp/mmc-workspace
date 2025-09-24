from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.opportunity_controller import OpportunityController
from schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=OpportunityResponse)
async def create_opportunity(
    opportunity: OpportunityCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = OpportunityController(db)
    return controller.create_opportunity(opportunity, tenant_id)

@router.get("/", response_model=List[OpportunityResponse])
async def get_opportunities(
    tenant_id: int = Depends(get_current_tenant_id),
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    controller = OpportunityController(db)
    return controller.get_opportunities(tenant_id, skip, limit, status)

@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = OpportunityController(db)
    return controller.get_opportunity(opportunity_id, tenant_id)

@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: int,
    opportunity_update: OpportunityUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = OpportunityController(db)
    return controller.update_opportunity(opportunity_id, opportunity_update, tenant_id)

@router.delete("/{opportunity_id}")
async def delete_opportunity(
    opportunity_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = OpportunityController(db)
    return controller.delete_opportunity(opportunity_id, tenant_id)