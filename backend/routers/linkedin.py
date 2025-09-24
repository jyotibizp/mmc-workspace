from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_user, get_current_tenant_id
from controllers.linkedin_controller import LinkedInController
from schemas.linkedin import LinkedInPostCreate, LinkedInPostResponse
from typing import List, Dict, Any

router = APIRouter()

@router.post("/ingest", response_model=LinkedInPostResponse)
async def ingest_linkedin_post(
    post_data: LinkedInPostCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = LinkedInController(db)
    return controller.ingest_linkedin_post(post_data, current_user, tenant_id)

@router.get("/posts", response_model=List[LinkedInPostResponse])
async def get_linkedin_posts(
    tenant_id: int = Depends(get_current_tenant_id),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    controller = LinkedInController(db)
    return controller.get_linkedin_posts(tenant_id, skip, limit)

@router.get("/posts/{post_id}", response_model=LinkedInPostResponse)
async def get_linkedin_post(
    post_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = LinkedInController(db)
    return controller.get_linkedin_post(post_id, tenant_id)