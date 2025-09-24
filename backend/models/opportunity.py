from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum

class OpportunityStatus(enum.Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    REPLIED = "Replied"
    WON = "Won"
    LOST = "Lost"

class Opportunity(BaseModel):
    __tablename__ = "opportunities"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"))
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="SET NULL"))
    source_post_id = Column(Integer, ForeignKey("linkedin_posts.id", ondelete="SET NULL"))
    title = Column(String(255), nullable=False)
    summary = Column(Text)
    status = Column(Enum(OpportunityStatus), default=OpportunityStatus.DRAFT, nullable=False)
    tags = Column(JSON, default=list)

    tenant = relationship("Tenant", back_populates="opportunities")
    company = relationship("Company", back_populates="opportunities")
    contact = relationship("Contact", back_populates="opportunities")
    source_post = relationship("LinkedInPost", back_populates="opportunities")
    proposal = relationship("Proposal", back_populates="opportunity", uselist=False)
    campaign_notes = relationship("CampaignNote", back_populates="opportunity", cascade="all, delete-orphan")