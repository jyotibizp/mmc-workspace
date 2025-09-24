from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    auth0_user_id = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255))
    role = Column(String(50), default="user")

    tenant = relationship("Tenant", back_populates="users")
    linkedin_posts = relationship("LinkedInPost", back_populates="user", cascade="all, delete-orphan")