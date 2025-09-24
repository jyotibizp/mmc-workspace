from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.contact_controller import ContactController
from schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.create_contact(contact, tenant_id)

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    tenant_id: int = Depends(get_current_tenant_id),
    company_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.get_contacts(tenant_id, skip, limit, company_id, search)

@router.get("/statistics")
async def get_contact_statistics(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.get_contact_statistics(tenant_id)

@router.get("/company/{company_id}", response_model=List[ContactResponse])
async def get_contacts_by_company(
    company_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.get_contacts_by_company(company_id, tenant_id)

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.get_contact(contact_id, tenant_id)

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.update_contact(contact_id, contact_update, tenant_id)

@router.post("/{primary_id}/merge/{secondary_id}", response_model=ContactResponse)
async def merge_contacts(
    primary_id: int,
    secondary_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.merge_contacts(primary_id, secondary_id, tenant_id)

@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = ContactController(db)
    return controller.delete_contact(contact_id, tenant_id)