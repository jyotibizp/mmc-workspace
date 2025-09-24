from sqlalchemy.orm import Session
from schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from services.campaign_service import CampaignService
from queries.campaign_queries import CampaignQueries
from utils.response_helpers import not_found_error, deletion_success
from typing import List, Optional

class CampaignController:
    def __init__(self, db: Session):
        self.db = db
        self.campaign_service = CampaignService(db)
        self.queries = CampaignQueries(db)

    def create_campaign(
        self,
        campaign: CampaignCreate,
        tenant_id: int
    ) -> CampaignResponse:
        """Create a new campaign."""
        campaign_data = campaign.model_dump()
        campaign_data["tenant_id"] = tenant_id

        # Use service for business logic and validation
        new_campaign = self.campaign_service.create_campaign_with_validation(campaign_data)
        return CampaignResponse.model_validate(new_campaign)

    def get_campaigns(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[CampaignResponse]:
        """Get campaigns with optional search."""
        if search:
            # Use service for business logic
            campaigns = self.campaign_service.search_campaigns_by_name(tenant_id, search)
        else:
            # Use queries directly for simple reads
            campaigns = self.queries.get_campaigns_by_tenant(tenant_id, skip, limit)

        return [CampaignResponse.model_validate(campaign) for campaign in campaigns]

    def get_campaign(
        self,
        campaign_id: int,
        tenant_id: int
    ) -> CampaignResponse:
        """Get a specific campaign."""
        # Use queries directly for simple reads
        campaign = self.queries.get_campaign_by_id(campaign_id, tenant_id)

        if not campaign:
            raise not_found_error("Campaign", campaign_id)

        return CampaignResponse.model_validate(campaign)

    def update_campaign(
        self,
        campaign_id: int,
        campaign_update: CampaignUpdate,
        tenant_id: int
    ) -> CampaignResponse:
        """Update an existing campaign."""
        campaign = self.queries.get_campaign_by_id(campaign_id, tenant_id)

        if not campaign:
            raise not_found_error("Campaign", campaign_id)

        update_data = campaign_update.model_dump(exclude_unset=True)

        # Use service for business validation
        updated_campaign = self.campaign_service.update_campaign_with_validation(campaign, update_data)

        return CampaignResponse.model_validate(updated_campaign)

    def delete_campaign(
        self,
        campaign_id: int,
        tenant_id: int
    ) -> dict:
        """Delete a campaign."""
        campaign = self.queries.get_campaign_by_id(campaign_id, tenant_id)

        if not campaign:
            raise not_found_error("Campaign", campaign_id)

        self.queries.delete_campaign(campaign)
        return deletion_success("Campaign")

    def archive_campaign(
        self,
        campaign_id: int,
        tenant_id: int
    ) -> CampaignResponse:
        """Archive a campaign (soft delete)."""
        campaign = self.queries.get_campaign_by_id(campaign_id, tenant_id)

        if not campaign:
            raise not_found_error("Campaign", campaign_id)

        # Use service for business logic
        archived_campaign = self.campaign_service.archive_campaign(campaign)
        return CampaignResponse.model_validate(archived_campaign)

    def get_campaign_statistics(
        self,
        tenant_id: int
    ) -> dict:
        """Get campaign statistics for tenant."""
        # Use service for business logic
        return self.campaign_service.get_campaign_statistics(tenant_id)