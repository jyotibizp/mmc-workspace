from sqlalchemy.orm import Session
from models import Campaign
from typing import Optional, List

class CampaignQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_campaign(self, campaign_data: dict) -> Campaign:
        """Create a new campaign."""
        new_campaign = Campaign(**campaign_data)
        self.db.add(new_campaign)
        self.db.commit()
        self.db.refresh(new_campaign)
        return new_campaign

    def get_campaigns_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """Get campaigns for a specific tenant with pagination."""
        return self.db.query(Campaign).filter(
            Campaign.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()

    def get_campaign_by_id(self, campaign_id: int, tenant_id: int) -> Optional[Campaign]:
        """Get a specific campaign by ID within tenant."""
        return self.db.query(Campaign).filter(
            Campaign.id == campaign_id,
            Campaign.tenant_id == tenant_id
        ).first()

    def update_campaign(self, campaign: Campaign, update_data: dict) -> Campaign:
        """Update an existing campaign."""
        for field, value in update_data.items():
            setattr(campaign, field, value)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def delete_campaign(self, campaign: Campaign) -> None:
        """Delete a campaign."""
        self.db.delete(campaign)
        self.db.commit()

    def get_campaigns_by_name(self, tenant_id: int, name: str) -> List[Campaign]:
        """Get campaigns by name (for duplicate checking)."""
        return self.db.query(Campaign).filter(
            Campaign.tenant_id == tenant_id,
            Campaign.name.ilike(f"%{name}%")
        ).all()

    def count_campaigns_by_tenant(self, tenant_id: int) -> int:
        """Count total campaigns for a tenant."""
        return self.db.query(Campaign).filter(
            Campaign.tenant_id == tenant_id
        ).count()