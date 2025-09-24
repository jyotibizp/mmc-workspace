from sqlalchemy.orm import Session
from queries.auth_queries import AuthQueries
from utils.auth_helpers import extract_user_info, get_tenant_id_from_token
from utils.validation import validate_email
from utils.response_helpers import validation_error
from typing import Dict, Any, Optional, Tuple

class AuthService:
    """Service for authentication-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = AuthQueries(db)

    def authenticate_or_create_user(self, current_user: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Authenticate existing user or create new user/tenant if first time.
        Returns: (user_data, is_new_user)
        """
        user_info = extract_user_info(current_user)
        auth0_user_id = user_info["auth0_user_id"]

        # Check if user exists
        existing_user = self.queries.get_user_by_auth0_id(auth0_user_id)

        if existing_user:
            # Update last login and return existing user
            updated_user = self.queries.update_user_last_login(existing_user)
            return self._format_user_response(updated_user), False

        # New user - create tenant and user
        return self._create_new_user_with_tenant(user_info), True

    def get_user_profile(self, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Get user profile with tenant information."""
        user_info = extract_user_info(current_user)
        auth0_user_id = user_info["auth0_user_id"]

        # Try to get user with explicit tenant from token
        tenant_id = get_tenant_id_from_token(current_user)
        if tenant_id:
            user = self.queries.get_user_by_auth0_id_and_tenant(auth0_user_id, tenant_id)
        else:
            user = self.queries.get_user_by_auth0_id(auth0_user_id)

        if not user:
            # Auto-create user if doesn't exist
            user_data, _ = self.authenticate_or_create_user(current_user)
            return user_data

        return self._format_user_response(user)

    def validate_tenant_access(self, current_user: Dict[str, Any], tenant_id: int) -> bool:
        """Validate if user has access to specific tenant."""
        user_info = extract_user_info(current_user)
        auth0_user_id = user_info["auth0_user_id"]

        user = self.queries.get_user_by_auth0_id_and_tenant(auth0_user_id, tenant_id)
        return user is not None

    def _create_new_user_with_tenant(self, user_info: Dict[str, str]) -> Dict[str, Any]:
        """Create new user with their own tenant."""
        # Validate user info
        self._validate_user_info(user_info)

        try:
            # Create tenant first
            tenant_name = self._generate_tenant_name(user_info)
            tenant_data = {
                "name": tenant_name,
                "settings": {"created_by": user_info["auth0_user_id"]}
            }
            new_tenant = self.queries.create_tenant(tenant_data)

            # Create user
            user_data = {
                "tenant_id": new_tenant.id,
                "auth0_user_id": user_info["auth0_user_id"],
                "email": user_info["email"],
                "name": user_info["name"],
                "role": "admin"  # First user in tenant is admin
            }
            new_user = self.queries.create_user(user_data)

            return self._format_user_response(new_user)

        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create user: {str(e)}")

    def _validate_user_info(self, user_info: Dict[str, str]) -> None:
        """Validate user information from Auth0 token."""
        if not user_info.get("auth0_user_id"):
            raise validation_error("Invalid Auth0 user ID")

        email = user_info.get("email", "")
        if not email or not validate_email(email):
            raise validation_error("Valid email address is required")

        if not user_info.get("name", "").strip():
            raise validation_error("User name is required")

    def _generate_tenant_name(self, user_info: Dict[str, str]) -> str:
        """Generate a unique tenant name for new user."""
        # Use email domain or fallback to user ID
        email = user_info.get("email", "")
        if email and "@" in email:
            domain = email.split("@")[1].replace(".", "_")
            base_name = f"tenant_{domain}"
        else:
            auth0_id = user_info["auth0_user_id"]
            base_name = f"tenant_{auth0_id[:8]}"

        return base_name

    def _format_user_response(self, user) -> Dict[str, Any]:
        """Format user data for API response."""
        return {
            "id": user.id,
            "tenant_id": user.tenant_id,
            "auth0_user_id": user.auth0_user_id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }