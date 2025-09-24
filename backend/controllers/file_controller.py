from sqlalchemy.orm import Session
from fastapi import UploadFile
from services.file_service import FileService
from queries.file_queries import FileQueries
from schemas.file import FileUploadResponse, ProposalFileResponse, FileStatisticsResponse, FileCleanupResponse
from utils.response_helpers import not_found_error
from typing import List, Optional

class FileController:
    def __init__(self, db: Session):
        self.db = db
        self.file_service = FileService(db)
        self.queries = FileQueries(db)

    async def upload_proposal_file(
        self,
        file: UploadFile,
        proposal_id: int,
        tenant_id: int
    ) -> FileUploadResponse:
        """Upload a file for a proposal."""
        # Use service for business logic and validation
        file_data = await self.file_service.upload_proposal_file(file, proposal_id, tenant_id)
        return FileUploadResponse(**file_data)

    def get_proposal_files(
        self,
        tenant_id: int,
        proposal_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProposalFileResponse]:
        """Get proposal files with optional proposal filter."""
        if proposal_id:
            # Get files for specific proposal
            files = self.queries.get_proposal_files_by_proposal(proposal_id, tenant_id)
        else:
            # Get all files for tenant
            files = self.queries.get_proposal_files_by_tenant(tenant_id, skip, limit)

        return [ProposalFileResponse.model_validate(file) for file in files]

    def get_proposal_file(
        self,
        file_id: int,
        tenant_id: int
    ) -> ProposalFileResponse:
        """Get a specific proposal file."""
        # Use queries directly for simple reads
        file = self.queries.get_proposal_file_by_id(file_id, tenant_id)

        if not file:
            raise not_found_error("File", file_id)

        return ProposalFileResponse.model_validate(file)

    def delete_file(
        self,
        filename: str,
        tenant_id: int
    ) -> dict:
        """Delete a file."""
        # Use service for business logic (handles both disk and DB)
        return self.file_service.delete_proposal_file(filename, tenant_id)

    def get_file_statistics(
        self,
        tenant_id: int
    ) -> FileStatisticsResponse:
        """Get file statistics for tenant."""
        # Use service for business logic
        stats = self.file_service.get_file_statistics(tenant_id)
        return FileStatisticsResponse(**stats)

    def cleanup_orphaned_files(
        self,
        tenant_id: int
    ) -> FileCleanupResponse:
        """Clean up orphaned files."""
        # Use service for business logic
        result = self.file_service.cleanup_orphaned_files(tenant_id)
        return FileCleanupResponse(**result)

    def get_file_by_filename(
        self,
        filename: str,
        tenant_id: int
    ) -> ProposalFileResponse:
        """Get file by filename."""
        # Use queries directly for simple reads
        file = self.queries.get_proposal_file_by_filename(filename, tenant_id)

        if not file:
            raise not_found_error("File")

        return ProposalFileResponse.model_validate(file)