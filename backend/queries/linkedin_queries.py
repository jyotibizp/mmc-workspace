from sqlalchemy.orm import Session
from models import LinkedInPost, User
from typing import Optional, List

class LinkedInQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_auth0_id(self, auth0_user_id: str, tenant_id: int) -> Optional[User]:
        return self.db.query(User).filter(
            User.auth0_user_id == auth0_user_id,
            User.tenant_id == tenant_id
        ).first()

    def get_post_by_url(self, post_url: str, tenant_id: int) -> Optional[LinkedInPost]:
        return self.db.query(LinkedInPost).filter(
            LinkedInPost.tenant_id == tenant_id,
            LinkedInPost.post_url == post_url
        ).first()

    def create_linkedin_post(self, post_data: dict) -> LinkedInPost:
        new_post = LinkedInPost(**post_data)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post

    def get_posts_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[LinkedInPost]:
        return self.db.query(LinkedInPost).filter(
            LinkedInPost.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()

    def get_post_by_id(self, post_id: int, tenant_id: int) -> Optional[LinkedInPost]:
        return self.db.query(LinkedInPost).filter(
            LinkedInPost.id == post_id,
            LinkedInPost.tenant_id == tenant_id
        ).first()