from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Contact(BaseModel):
    __tablename__ = "contacts"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), index=True)
    phone = Column(String(50))
    linkedin_profile_url = Column(String(512), index=True)

    tenant = relationship("Tenant")
    company = relationship("Company", back_populates="contacts")
    opportunities = relationship("Opportunity", back_populates="contact")