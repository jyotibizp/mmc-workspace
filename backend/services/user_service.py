from sqlalchemy.orm import Session
from queries.linkedin_queries import LinkedInQueries
from models import User, Tenant
from utils.response_helpers import not_found_error
from utils.auth_helpers import extract_user_info
from typing import Dict, Any

class UserService:
    """Service for user-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = LinkedInQueries(db)

    def get_or_create_user(self, current_user: Dict[str, Any], tenant_id: int) -> User:
        """Get existing user or create new one if doesn't exist."""
        user_info = extract_user_info(current_user)
        auth0_user_id = user_info["auth0_user_id"]

        user = self.queries.get_user_by_auth0_id(auth0_user_id, tenant_id)

        if not user:
            # Auto-create user if doesn't exist
            user = User(
                tenant_id=tenant_id,
                auth0_user_id=auth0_user_id,
                email=user_info["email"],
                name=user_info["name"],
                role="user"
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        return user

    def validate_user_access(self, current_user: Dict[str, Any], tenant_id: int) -> User:
        """Validate user exists and has access to tenant."""
        user_info = extract_user_info(current_user)
        auth0_user_id = user_info["auth0_user_id"]

        user = self.queries.get_user_by_auth0_id(auth0_user_id, tenant_id)
        if not user:
            raise not_found_error("User")

        return user