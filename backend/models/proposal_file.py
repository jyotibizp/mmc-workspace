from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class ProposalFile(BaseModel):
    __tablename__ = "proposal_files"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(String(512), nullable=False)

    tenant = relationship("Tenant")
    proposal = relationship("Proposal", back_populates="files")