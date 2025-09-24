from sqlalchemy.orm import Session
from models import User, Tenant
from typing import Optional

class AuthQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_auth0_id(self, auth0_user_id: str) -> Optional[User]:
        """Get user by Auth0 user ID across all tenants."""
        return self.db.query(User).filter(
            User.auth0_user_id == auth0_user_id
        ).first()

    def get_user_by_auth0_id_and_tenant(self, auth0_user_id: str, tenant_id: int) -> Optional[User]:
        """Get user by Auth0 user ID within specific tenant."""
        return self.db.query(User).filter(
            User.auth0_user_id == auth0_user_id,
            User.tenant_id == tenant_id
        ).first()

    def create_tenant(self, tenant_data: dict) -> Tenant:
        """Create a new tenant."""
        new_tenant = Tenant(**tenant_data)
        self.db.add(new_tenant)
        self.db.flush()  # Get ID without committing
        return new_tenant

    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        new_user = User(**user_data)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_tenant_by_id(self, tenant_id: int) -> Optional[Tenant]:
        """Get tenant by ID."""
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def update_user_last_login(self, user: User) -> User:
        """Update user's last login timestamp."""
        from sqlalchemy.sql import func
        user.updated_at = func.now()
        self.db.commit()
        self.db.refresh(user)
        return user