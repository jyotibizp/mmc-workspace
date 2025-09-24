from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from models.base import BaseModel
import enum

class ProposalStatus(enum.Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    REPLIED = "Replied"
    WON = "Won"
    LOST = "Lost"

class Proposal(BaseModel):
    __tablename__ = "proposals"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.DRAFT, nullable=False)

    tenant = relationship("Tenant", back_populates="proposals")
    opportunity = relationship("Opportunity", back_populates="proposal")
    files = relationship("ProposalFile", back_populates="proposal", cascade="all, delete-orphan")