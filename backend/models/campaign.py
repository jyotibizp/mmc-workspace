from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Campaign(BaseModel):
    __tablename__ = "campaigns"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    tenant = relationship("Tenant", back_populates="campaigns")
    notes = relationship("CampaignNote", back_populates="campaign", cascade="all, delete-orphan")