from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Company(BaseModel):
    __tablename__ = "companies"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255))
    linkedin_url = Column(String(512))

    tenant = relationship("Tenant", back_populates="companies")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="company")