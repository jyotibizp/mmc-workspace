from sqlalchemy.orm import Session
from models import Campaign, CampaignNote
from typing import Optional, List
from datetime import datetime

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

    # Campaign Notes methods
    def create_campaign_note(self, note_data: dict) -> CampaignNote:
        """Create a new campaign note."""
        new_note = CampaignNote(**note_data)
        self.db.add(new_note)
        self.db.commit()
        self.db.refresh(new_note)
        return new_note

    def get_campaign_notes(self, campaign_id: int, tenant_id: int) -> List[CampaignNote]:
        """Get all notes for a specific campaign."""
        return self.db.query(CampaignNote).filter(
            CampaignNote.campaign_id == campaign_id,
            CampaignNote.tenant_id == tenant_id
        ).order_by(CampaignNote.created_at.desc()).all()

    def get_campaign_note_by_id(self, note_id: int, tenant_id: int) -> Optional[CampaignNote]:
        """Get a specific campaign note by ID."""
        return self.db.query(CampaignNote).filter(
            CampaignNote.id == note_id,
            CampaignNote.tenant_id == tenant_id
        ).first()

    def update_campaign_note(self, note: CampaignNote, update_data: dict) -> CampaignNote:
        """Update an existing campaign note."""
        for field, value in update_data.items():
            setattr(note, field, value)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_campaign_note(self, note: CampaignNote) -> None:
        """Delete a campaign note."""
        self.db.delete(note)
        self.db.commit()

    def get_overdue_follow_ups(self, tenant_id: int) -> List[CampaignNote]:
        """Get overdue follow-up notes for a tenant."""
        now = datetime.now()
        return self.db.query(CampaignNote).filter(
            CampaignNote.tenant_id == tenant_id,
            CampaignNote.follow_up_at < now,
            CampaignNote.completed == False
        ).order_by(CampaignNote.follow_up_at.asc()).all()

    def get_notes_by_opportunity(self, opportunity_id: int, tenant_id: int) -> List[CampaignNote]:
        """Get all notes for a specific opportunity."""
        return self.db.query(CampaignNote).filter(
            CampaignNote.opportunity_id == opportunity_id,
            CampaignNote.tenant_id == tenant_id
        ).order_by(CampaignNote.created_at.desc()).all()