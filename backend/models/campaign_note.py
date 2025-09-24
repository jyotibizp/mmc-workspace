from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel

class CampaignNote(BaseModel):
    __tablename__ = "campaign_notes"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=False)
    follow_up_at = Column(DateTime(timezone=True))
    completed = Column(Boolean, default=False, nullable=False)

    tenant = relationship("Tenant")
    campaign = relationship("Campaign", back_populates="notes")
    opportunity = relationship("Opportunity", back_populates="campaign_notes")