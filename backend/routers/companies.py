from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.company_controller import CompanyController
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CompanyController(db)
    return controller.create_company(company, tenant_id)

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    tenant_id: int = Depends(get_current_tenant_id),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    controller = CompanyController(db)
    return controller.get_companies(tenant_id, skip, limit)

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CompanyController(db)
    return controller.get_company(company_id, tenant_id)

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CompanyController(db)
    return controller.update_company(company_id, company_update, tenant_id)

@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = CompanyController(db)
    return controller.delete_company(company_id, tenant_id)