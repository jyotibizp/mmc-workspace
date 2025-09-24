from sqlalchemy.orm import Session
from schemas.proposal import ProposalCreate, ProposalUpdate, ProposalResponse
from services.proposal_service import ProposalService
from queries.proposal_queries import ProposalQueries
from utils.response_helpers import not_found_error, deletion_success
from typing import List, Optional

class ProposalController:
    def __init__(self, db: Session):
        self.db = db
        self.proposal_service = ProposalService(db)
        self.queries = ProposalQueries(db)

    def create_proposal(
        self,
        proposal: ProposalCreate,
        tenant_id: int
    ) -> ProposalResponse:
        """Create a new proposal."""
        proposal_data = proposal.model_dump()
        proposal_data["tenant_id"] = tenant_id

        # Use service for business logic and validation
        new_proposal = self.proposal_service.create_proposal_with_validation(proposal_data)
        return ProposalResponse.model_validate(new_proposal)

    async def generate_proposal_with_ai(
        self,
        opportunity_id: int,
        tenant_id: int,
        additional_context: Optional[str] = None
    ) -> dict:
        """Generate proposal using AI service."""
        # Use service for business logic
        result = await self.proposal_service.generate_proposal_with_ai(
            opportunity_id, tenant_id, additional_context
        )

        return {
            "proposal": ProposalResponse.model_validate(result["proposal"]),
            "ai_suggestions": result["ai_suggestions"]
        }

    def get_proposals(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[ProposalResponse]:
        """Get proposals with optional filters."""
        if search:
            # Use service for business logic
            proposals = self.proposal_service.search_proposals(tenant_id, search)
        else:
            # Use queries directly for simple reads
            proposals = self.queries.get_proposals_by_tenant(tenant_id, skip, limit, status)

        return [ProposalResponse.model_validate(proposal) for proposal in proposals]

    def get_proposal(
        self,
        proposal_id: int,
        tenant_id: int
    ) -> ProposalResponse:
        """Get a specific proposal."""
        # Use queries directly for simple reads
        proposal = self.queries.get_proposal_by_id(proposal_id, tenant_id)

        if not proposal:
            raise not_found_error("Proposal", proposal_id)

        return ProposalResponse.model_validate(proposal)

    def update_proposal(
        self,
        proposal_id: int,
        proposal_update: ProposalUpdate,
        tenant_id: int
    ) -> ProposalResponse:
        """Update an existing proposal."""
        proposal = self.queries.get_proposal_by_id(proposal_id, tenant_id)

        if not proposal:
            raise not_found_error("Proposal", proposal_id)

        update_data = proposal_update.model_dump(exclude_unset=True)

        # Use service for business validation
        updated_proposal = self.proposal_service.update_proposal_with_validation(proposal, update_data)

        return ProposalResponse.model_validate(updated_proposal)

    def delete_proposal(
        self,
        proposal_id: int,
        tenant_id: int
    ) -> dict:
        """Delete a proposal."""
        proposal = self.queries.get_proposal_by_id(proposal_id, tenant_id)

        if not proposal:
            raise not_found_error("Proposal", proposal_id)

        self.queries.delete_proposal(proposal)
        return deletion_success("Proposal")

    def get_proposal_statistics(
        self,
        tenant_id: int
    ) -> dict:
        """Get proposal statistics for tenant."""
        # Use service for business logic
        return self.proposal_service.get_proposal_statistics(tenant_id)

    def duplicate_proposal(
        self,
        proposal_id: int,
        new_opportunity_id: int,
        tenant_id: int
    ) -> ProposalResponse:
        """Duplicate an existing proposal for a new opportunity."""
        # Use service for business logic
        duplicated_proposal = self.proposal_service.duplicate_proposal(
            proposal_id, tenant_id, new_opportunity_id
        )
        return ProposalResponse.model_validate(duplicated_proposal)

    def export_proposal(
        self,
        proposal_id: int,
        tenant_id: int,
        format: str = "markdown"
    ) -> dict:
        """Export proposal in different formats."""
        # Use service for business logic
        return self.proposal_service.export_proposal(proposal_id, tenant_id, format)

    def get_proposal_by_opportunity(
        self,
        opportunity_id: int,
        tenant_id: int
    ) -> Optional[ProposalResponse]:
        """Get proposal by opportunity ID."""
        # Use queries directly for simple reads
        proposal = self.queries.get_proposal_by_opportunity_id(opportunity_id, tenant_id)

        if not proposal:
            return None

        return ProposalResponse.model_validate(proposal)