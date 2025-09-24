from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.file_controller import FileController
from schemas.file import FileUploadResponse, ProposalFileResponse, FileStatisticsResponse, FileCleanupResponse
from typing import List, Optional

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_proposal_file(
    file: UploadFile = File(...),
    proposal_id: int = Query(..., description="Proposal ID to associate with the file"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return await controller.upload_proposal_file(file, proposal_id, tenant_id)

@router.get("/", response_model=List[ProposalFileResponse])
async def get_proposal_files(
    tenant_id: int = Depends(get_current_tenant_id),
    proposal_id: Optional[int] = Query(None, description="Filter by proposal ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.get_proposal_files(tenant_id, proposal_id, skip, limit)

@router.get("/statistics", response_model=FileStatisticsResponse)
async def get_file_statistics(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.get_file_statistics(tenant_id)

@router.post("/cleanup", response_model=FileCleanupResponse)
async def cleanup_orphaned_files(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.cleanup_orphaned_files(tenant_id)

@router.get("/{file_id}", response_model=ProposalFileResponse)
async def get_proposal_file(
    file_id: int,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.get_proposal_file(file_id, tenant_id)

@router.get("/by-filename/{filename}", response_model=ProposalFileResponse)
async def get_file_by_filename(
    filename: str,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.get_file_by_filename(filename, tenant_id)

@router.delete("/{filename}")
async def delete_file(
    filename: str,
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    controller = FileController(db)
    return controller.delete_file(filename, tenant_id)