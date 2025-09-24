from sqlalchemy.orm import Session
from queries.proposal_queries import ProposalQueries
from queries.opportunity_queries import OpportunityQueries
from services.ai_service import AIService
from utils.response_helpers import validation_error, conflict_error, not_found_error
from typing import Dict, Any, List, Optional

class ProposalService:
    """Service for proposal-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = ProposalQueries(db)
        self.opportunity_queries = OpportunityQueries(db)
        self.ai_service = AIService(db)

    def create_proposal_with_validation(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create proposal with business validation."""
        self._validate_proposal_data(proposal_data)
        self._validate_opportunity_exists(proposal_data)
        self._check_proposal_uniqueness(proposal_data)
        self._normalize_proposal_data(proposal_data)

        return self.queries.create_proposal(proposal_data)

    def update_proposal_with_validation(self, proposal: Any, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update proposal with business validation."""
        if update_data:
            self._validate_proposal_data(update_data, is_update=True)

            # Validate status transitions
            if "status" in update_data:
                self._validate_status_transition(proposal.status, update_data["status"])

            self._normalize_proposal_data(update_data)

        return self.queries.update_proposal(proposal, update_data)

    async def generate_proposal_with_ai(
        self,
        opportunity_id: int,
        tenant_id: int,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate proposal content using AI service."""
        # Validate opportunity exists
        opportunity = self.opportunity_queries.get_opportunity_by_id(opportunity_id, tenant_id)
        if not opportunity:
            raise not_found_error("Opportunity", opportunity_id)

        # Check if proposal already exists
        existing_proposal = self.queries.get_proposal_by_opportunity_id(opportunity_id, tenant_id)
        if existing_proposal:
            raise conflict_error("Proposal already exists for this opportunity")

        # Generate content using AI
        ai_result = await self.ai_service.generate_proposal(opportunity_id, tenant_id, None, additional_context)

        # Create proposal with AI-generated content
        proposal_data = {
            "tenant_id": tenant_id,
            "opportunity_id": opportunity_id,
            "content": ai_result["proposal_content"],
            "status": "Draft"
        }

        new_proposal = self.queries.create_proposal(proposal_data)

        return {
            "proposal": new_proposal,
            "ai_suggestions": ai_result.get("suggested_sections", [])
        }

    def get_proposal_statistics(self, tenant_id: int) -> Dict[str, Any]:
        """Get proposal statistics for a tenant."""
        total_proposals = self.queries.count_proposals_by_tenant(tenant_id)

        status_counts = {}
        for status in ["Draft", "Sent", "Replied", "Won", "Lost"]:
            status_counts[status.lower()] = self.queries.count_proposals_by_status(tenant_id, status)

        win_rate = 0
        if status_counts["sent"] + status_counts["replied"] + status_counts["won"] + status_counts["lost"] > 0:
            total_submitted = status_counts["sent"] + status_counts["replied"] + status_counts["won"] + status_counts["lost"]
            win_rate = round((status_counts["won"] / total_submitted) * 100, 2)

        return {
            "total_proposals": total_proposals,
            "status_breakdown": status_counts,
            "win_rate_percent": win_rate,
            "active_proposals": status_counts["draft"] + status_counts["sent"] + status_counts["replied"]
        }

    def search_proposals(self, tenant_id: int, search_term: str) -> List[Dict[str, Any]]:
        """Search proposals by content."""
        if len(search_term.strip()) < 3:
            raise validation_error("Search term must be at least 3 characters")

        proposals = self.queries.search_proposals_by_content(tenant_id, search_term)
        return proposals

    def duplicate_proposal(self, proposal_id: int, tenant_id: int, new_opportunity_id: int) -> Dict[str, Any]:
        """Duplicate an existing proposal for a new opportunity."""
        # Get original proposal
        original_proposal = self.queries.get_proposal_by_id(proposal_id, tenant_id)
        if not original_proposal:
            raise not_found_error("Proposal", proposal_id)

        # Validate new opportunity exists
        new_opportunity = self.opportunity_queries.get_opportunity_by_id(new_opportunity_id, tenant_id)
        if not new_opportunity:
            raise not_found_error("Opportunity", new_opportunity_id)

        # Check if proposal already exists for new opportunity
        existing_proposal = self.queries.get_proposal_by_opportunity_id(new_opportunity_id, tenant_id)
        if existing_proposal:
            raise conflict_error("Proposal already exists for the target opportunity")

        # Create new proposal with duplicated content
        proposal_data = {
            "tenant_id": tenant_id,
            "opportunity_id": new_opportunity_id,
            "content": original_proposal.content,
            "status": "Draft"
        }

        return self.queries.create_proposal(proposal_data)

    def export_proposal(self, proposal_id: int, tenant_id: int, format: str = "markdown") -> Dict[str, Any]:
        """Export proposal in different formats."""
        proposal = self.queries.get_proposal_by_id(proposal_id, tenant_id)
        if not proposal:
            raise not_found_error("Proposal", proposal_id)

        if format.lower() == "markdown":
            content = proposal.content
        elif format.lower() == "html":
            # Convert to basic HTML
            content = proposal.content.replace("\n", "<br>\n")
            content = f"<html><body>{content}</body></html>"
        elif format.lower() == "text":
            # Strip any formatting
            content = proposal.content
        else:
            raise validation_error("Unsupported export format. Use: markdown, html, text")

        return {
            "content": content,
            "format": format.lower(),
            "filename": f"proposal_{proposal.id}.{format.lower()}"
        }

    def _validate_proposal_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """Validate proposal data according to business rules."""
        # Content validation
        content = data.get("content")
        if not is_update and not content:
            raise validation_error("Proposal content is required")

        if content:
            content = content.strip()
            if len(content) < 50:
                raise validation_error("Proposal content must be at least 50 characters")
            if len(content) > 50000:
                raise validation_error("Proposal content must be less than 50,000 characters")

        # Status validation
        status = data.get("status")
        if status:
            valid_statuses = ["Draft", "Sent", "Replied", "Won", "Lost"]
            if status not in valid_statuses:
                raise validation_error(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    def _normalize_proposal_data(self, data: Dict[str, Any]) -> None:
        """Normalize proposal data for consistency."""
        # Normalize content (trim whitespace, ensure proper line endings)
        if "content" in data and data["content"]:
            data["content"] = data["content"].strip()

        # Normalize status (ensure proper case)
        if "status" in data and data["status"]:
            data["status"] = data["status"].capitalize()

    def _validate_opportunity_exists(self, proposal_data: Dict[str, Any]) -> None:
        """Validate that the opportunity exists."""
        opportunity_id = proposal_data["opportunity_id"]
        tenant_id = proposal_data["tenant_id"]

        opportunity = self.opportunity_queries.get_opportunity_by_id(opportunity_id, tenant_id)
        if not opportunity:
            raise not_found_error("Opportunity", opportunity_id)

    def _check_proposal_uniqueness(self, proposal_data: Dict[str, Any]) -> None:
        """Check if proposal already exists for this opportunity."""
        opportunity_id = proposal_data["opportunity_id"]
        tenant_id = proposal_data["tenant_id"]

        existing_proposal = self.queries.get_proposal_by_opportunity_id(opportunity_id, tenant_id)
        if existing_proposal:
            raise conflict_error("Proposal already exists for this opportunity")

    def _validate_status_transition(self, current_status: str, new_status: str) -> None:
        """Validate if status transition is allowed."""
        valid_transitions = {
            "Draft": ["Sent", "Lost"],
            "Sent": ["Replied", "Lost"],
            "Replied": ["Won", "Lost"],
            "Won": [],  # Terminal state
            "Lost": []  # Terminal state
        }

        if new_status not in valid_transitions.get(current_status, []):
            raise validation_error(f"Invalid status transition from {current_status} to {new_status}")