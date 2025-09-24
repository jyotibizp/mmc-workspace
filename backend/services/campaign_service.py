from sqlalchemy.orm import Session
from queries.campaign_queries import CampaignQueries
from utils.response_helpers import validation_error, conflict_error
from typing import Dict, Any, List, Optional

class CampaignService:
    """Service for campaign-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = CampaignQueries(db)

    def create_campaign_with_validation(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create campaign with business validation."""
        self._validate_campaign_data(campaign_data)
        self._check_campaign_name_uniqueness(campaign_data)
        self._normalize_campaign_data(campaign_data)

        return self.queries.create_campaign(campaign_data)

    def update_campaign_with_validation(self, campaign: Any, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update campaign with business validation."""
        if update_data:
            self._validate_campaign_data(update_data, is_update=True)

            # Check name uniqueness if name is being updated
            if "name" in update_data:
                self._check_campaign_name_uniqueness_for_update(
                    campaign.tenant_id, update_data["name"], campaign.id
                )

            self._normalize_campaign_data(update_data)

        return self.queries.update_campaign(campaign, update_data)

    def get_campaign_statistics(self, tenant_id: int) -> Dict[str, Any]:
        """Get campaign statistics for a tenant."""
        total_campaigns = self.queries.count_campaigns_by_tenant(tenant_id)

        return {
            "total_campaigns": total_campaigns,
            "active_campaigns": total_campaigns,  # For now, all campaigns are considered active
            "avg_campaigns_per_month": round(total_campaigns / 12, 2) if total_campaigns > 0 else 0
        }

    def search_campaigns_by_name(self, tenant_id: int, search_term: str) -> List[Dict[str, Any]]:
        """Search campaigns by name."""
        if len(search_term.strip()) < 2:
            raise validation_error("Search term must be at least 2 characters")

        campaigns = self.queries.get_campaigns_by_name(tenant_id, search_term)
        return campaigns

    def archive_campaign(self, campaign: Any) -> Dict[str, Any]:
        """Archive a campaign (business logic for soft delete)."""
        # For now, we'll just add a note to the description
        # In a full implementation, you might have an 'archived' status
        current_description = campaign.description or ""
        if not current_description.startswith("[ARCHIVED]"):
            archived_description = f"[ARCHIVED] {current_description}".strip()
            update_data = {"description": archived_description}
            return self.queries.update_campaign(campaign, update_data)

        return campaign

    def _validate_campaign_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """Validate campaign data according to business rules."""
        # Name validation
        name = data.get("name")
        if not is_update and not name:
            raise validation_error("Campaign name is required")

        if name:
            name = name.strip()
            if len(name) < 3:
                raise validation_error("Campaign name must be at least 3 characters")
            if len(name) > 100:
                raise validation_error("Campaign name must be less than 100 characters")

        # Description validation
        description = data.get("description")
        if description and len(description) > 1000:
            raise validation_error("Campaign description must be less than 1000 characters")

    def _normalize_campaign_data(self, data: Dict[str, Any]) -> None:
        """Normalize campaign data for consistency."""
        # Normalize name (trim whitespace, title case)
        if "name" in data and data["name"]:
            data["name"] = data["name"].strip().title()

        # Normalize description (trim whitespace)
        if "description" in data and data["description"]:
            data["description"] = data["description"].strip()

    def _check_campaign_name_uniqueness(self, campaign_data: Dict[str, Any]) -> None:
        """Check if campaign name already exists for this tenant."""
        tenant_id = campaign_data["tenant_id"]
        name = campaign_data.get("name", "").strip().lower()

        if name:
            existing_campaigns = self.queries.get_campaigns_by_name(tenant_id, name)
            for existing in existing_campaigns:
                if existing.name.lower() == name:
                    raise conflict_error(f"Campaign with name '{campaign_data['name']}' already exists")

    def _check_campaign_name_uniqueness_for_update(self, tenant_id: int, new_name: str, campaign_id: int) -> None:
        """Check campaign name uniqueness during update (excluding current campaign)."""
        name = new_name.strip().lower()
        existing_campaigns = self.queries.get_campaigns_by_name(tenant_id, name)

        for existing in existing_campaigns:
            if existing.name.lower() == name and existing.id != campaign_id:
                raise conflict_error(f"Campaign with name '{new_name}' already exists")