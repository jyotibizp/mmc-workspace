from sqlalchemy.orm import Session
from models import ProposalFile
from typing import Optional, List

class FileQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_proposal_file(self, file_data: dict) -> ProposalFile:
        """Create a new proposal file record."""
        new_file = ProposalFile(**file_data)
        self.db.add(new_file)
        self.db.commit()
        self.db.refresh(new_file)
        return new_file

    def get_proposal_files_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[ProposalFile]:
        """Get all proposal files for a tenant."""
        return self.db.query(ProposalFile).filter(
            ProposalFile.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()

    def get_proposal_files_by_proposal(self, proposal_id: int, tenant_id: int) -> List[ProposalFile]:
        """Get all files for a specific proposal."""
        return self.db.query(ProposalFile).filter(
            ProposalFile.proposal_id == proposal_id,
            ProposalFile.tenant_id == tenant_id
        ).all()

    def get_proposal_file_by_id(self, file_id: int, tenant_id: int) -> Optional[ProposalFile]:
        """Get a specific proposal file by ID."""
        return self.db.query(ProposalFile).filter(
            ProposalFile.id == file_id,
            ProposalFile.tenant_id == tenant_id
        ).first()

    def get_proposal_file_by_filename(self, filename: str, tenant_id: int) -> Optional[ProposalFile]:
        """Get proposal file by filename within tenant."""
        return self.db.query(ProposalFile).filter(
            ProposalFile.filename == filename,
            ProposalFile.tenant_id == tenant_id
        ).first()

    def delete_proposal_file(self, proposal_file: ProposalFile) -> None:
        """Delete a proposal file record."""
        self.db.delete(proposal_file)
        self.db.commit()

    def update_proposal_file(self, proposal_file: ProposalFile, update_data: dict) -> ProposalFile:
        """Update a proposal file record."""
        for field, value in update_data.items():
            setattr(proposal_file, field, value)
        self.db.commit()
        self.db.refresh(proposal_file)
        return proposal_file

    def count_files_by_tenant(self, tenant_id: int) -> int:
        """Count total files for a tenant."""
        return self.db.query(ProposalFile).filter(
            ProposalFile.tenant_id == tenant_id
        ).count()

    def get_total_storage_used(self, tenant_id: int) -> int:
        """Get total storage used by a tenant in bytes."""
        result = self.db.query(
            self.db.func.sum(ProposalFile.size)
        ).filter(
            ProposalFile.tenant_id == tenant_id
        ).scalar()
        return result or 0