from sqlalchemy.orm import Session
from queries.opportunity_queries import OpportunityQueries
from utils.response_helpers import not_found_error
from typing import Dict, Any, List, Optional

class OpportunityService:
    """Service for opportunity-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = OpportunityQueries(db)

    def create_opportunity_with_validation(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create opportunity with business validation."""
        # Add any business rules here
        self._validate_opportunity_data(opportunity_data)

        return self.queries.create_opportunity(opportunity_data)

    def update_opportunity_status(self, opportunity_id: int, tenant_id: int, new_status: str) -> Dict[str, Any]:
        """Update opportunity status with business logic."""
        opportunity = self.queries.get_opportunity_by_id(opportunity_id, tenant_id)
        if not opportunity:
            raise not_found_error("Opportunity", opportunity_id)

        # Add status transition validation if needed
        self._validate_status_transition(opportunity.status, new_status)

        update_data = {"status": new_status}
        return self.queries.update_opportunity(opportunity, update_data)

    def get_opportunities_by_status(self, tenant_id: int, status: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get opportunities filtered by status."""
        return self.queries.get_opportunities_by_tenant(tenant_id, skip, limit, status)

    def _validate_opportunity_data(self, data: Dict[str, Any]) -> None:
        """Validate opportunity data according to business rules."""
        # Add business validation logic here
        if not data.get("title"):
            raise ValueError("Opportunity title is required")

    def _validate_status_transition(self, current_status: str, new_status: str) -> None:
        """Validate if status transition is allowed."""
        # Add status transition rules here
        valid_transitions = {
            "Draft": ["Sent", "Lost"],
            "Sent": ["Replied", "Lost"],
            "Replied": ["Won", "Lost"],
            "Won": [],  # Terminal state
            "Lost": []  # Terminal state
        }

        if new_status not in valid_transitions.get(current_status, []):
            raise ValueError(f"Invalid status transition from {current_status} to {new_status}")