from typing import Dict, Any, Optional

def extract_user_info(current_user: Dict[str, Any]) -> Dict[str, str]:
    """Extract standardized user information from Auth0 token."""
    return {
        "auth0_user_id": current_user.get("sub", ""),
        "email": current_user.get("email", ""),
        "name": current_user.get("name", ""),
        "tenant_id": current_user.get("https://mapmyclient.com/tenant_id")
    }

def get_tenant_id_from_token(current_user: Dict[str, Any]) -> Optional[int]:
    """Extract tenant ID from Auth0 token."""
    return current_user.get("https://mapmyclient.com/tenant_id")