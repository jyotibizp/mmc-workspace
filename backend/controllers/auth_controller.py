from sqlalchemy.orm import Session
from services.auth_service import AuthService
from utils.response_helpers import success_message
from typing import Dict, Any

class AuthController:
    """Controller for authentication operations."""

    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)

    def get_me(self, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Get current user profile with auto-creation if needed."""
        return self.auth_service.get_user_profile(current_user)

    def authenticate_user(self, current_user: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate user and create if first time login."""
        user_data, is_new_user = self.auth_service.authenticate_or_create_user(current_user)

        response = {
            "user": user_data,
            "is_new_user": is_new_user
        }

        if is_new_user:
            response["message"] = "Welcome! Your account has been created."
        else:
            response["message"] = "Welcome back!"

        return response

    def logout(self) -> Dict[str, str]:
        """Handle user logout."""
        # In JWT-based auth, logout is typically handled client-side
        # This endpoint is mainly for consistency and potential future use
        return success_message("completed", "Logout")

    def validate_access(self, current_user: Dict[str, Any], tenant_id: int) -> Dict[str, Any]:
        """Validate user access to specific tenant."""
        has_access = self.auth_service.validate_tenant_access(current_user, tenant_id)

        return {
            "has_access": has_access,
            "tenant_id": tenant_id,
            "user_id": current_user.get("sub")
        }