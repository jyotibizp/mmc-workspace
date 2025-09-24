from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from models.base import BaseModel

class Tenant(BaseModel):
    __tablename__ = "tenants"

    name = Column(String(255), nullable=False, unique=True)
    settings = Column(JSON, default={})

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    linkedin_posts = relationship("LinkedInPost", back_populates="tenant", cascade="all, delete-orphan")
    companies = relationship("Company", back_populates="tenant", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="tenant", cascade="all, delete-orphan")
    proposals = relationship("Proposal", back_populates="tenant", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="tenant", cascade="all, delete-orphan")