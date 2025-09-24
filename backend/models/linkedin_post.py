from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import BaseModel

class LinkedInPost(BaseModel):
    __tablename__ = "linkedin_posts"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'post_url', name='uq_tenant_post_url'),
    )

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    post_url = Column(String(512), nullable=False, index=True)
    author_profile_url = Column(String(512))
    content = Column(Text)
    scraped_at = Column(DateTime(timezone=True), nullable=False)

    tenant = relationship("Tenant", back_populates="linkedin_posts")
    user = relationship("User", back_populates="linkedin_posts")
    opportunities = relationship("Opportunity", back_populates="source_post")