from sqlalchemy.orm import Session
from models import Proposal
from typing import Optional, List

class ProposalQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_proposal(self, proposal_data: dict) -> Proposal:
        """Create a new proposal."""
        new_proposal = Proposal(**proposal_data)
        self.db.add(new_proposal)
        self.db.commit()
        self.db.refresh(new_proposal)
        return new_proposal

    def get_proposals_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Proposal]:
        """Get proposals for a specific tenant with optional status filter."""
        query = self.db.query(Proposal).filter(Proposal.tenant_id == tenant_id)

        if status:
            query = query.filter(Proposal.status == status)

        return query.offset(skip).limit(limit).all()

    def get_proposal_by_id(self, proposal_id: int, tenant_id: int) -> Optional[Proposal]:
        """Get a specific proposal by ID within tenant."""
        return self.db.query(Proposal).filter(
            Proposal.id == proposal_id,
            Proposal.tenant_id == tenant_id
        ).first()

    def get_proposal_by_opportunity_id(self, opportunity_id: int, tenant_id: int) -> Optional[Proposal]:
        """Get proposal by opportunity ID within tenant."""
        return self.db.query(Proposal).filter(
            Proposal.opportunity_id == opportunity_id,
            Proposal.tenant_id == tenant_id
        ).first()

    def update_proposal(self, proposal: Proposal, update_data: dict) -> Proposal:
        """Update an existing proposal."""
        for field, value in update_data.items():
            setattr(proposal, field, value)
        self.db.commit()
        self.db.refresh(proposal)
        return proposal

    def delete_proposal(self, proposal: Proposal) -> None:
        """Delete a proposal."""
        self.db.delete(proposal)
        self.db.commit()

    def get_proposals_by_status(self, tenant_id: int, status: str) -> List[Proposal]:
        """Get proposals by status."""
        return self.db.query(Proposal).filter(
            Proposal.tenant_id == tenant_id,
            Proposal.status == status
        ).all()

    def count_proposals_by_tenant(self, tenant_id: int) -> int:
        """Count total proposals for a tenant."""
        return self.db.query(Proposal).filter(
            Proposal.tenant_id == tenant_id
        ).count()

    def count_proposals_by_status(self, tenant_id: int, status: str) -> int:
        """Count proposals by status for a tenant."""
        return self.db.query(Proposal).filter(
            Proposal.tenant_id == tenant_id,
            Proposal.status == status
        ).count()

    def search_proposals_by_content(self, tenant_id: int, search_term: str) -> List[Proposal]:
        """Search proposals by content."""
        return self.db.query(Proposal).filter(
            Proposal.tenant_id == tenant_id,
            Proposal.content.ilike(f"%{search_term}%")
        ).all()