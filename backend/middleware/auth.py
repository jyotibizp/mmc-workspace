from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
from typing import Optional, Dict, Any
from database import settings
import logging
import os

logger = logging.getLogger(__name__)

# Enable demo mode for testing without Auth0
DEMO_MODE = settings.demo_mode.lower() == "true"

security = HTTPBearer(auto_error=False)

class Auth0JWTBearer:
    def __init__(self):
        self.domain = settings.auth0_domain
        self.api_audience = settings.auth0_api_audience
        self.algorithms = [settings.auth0_algorithms]
        self.jwks_client = None
        self.jwks = None

    async def get_jwks(self):
        if not self.jwks:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{self.domain}/.well-known/jwks.json")
                self.jwks = response.json()
        return self.jwks

    async def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            jwks = await self.get_jwks()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break

            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find appropriate key"
                )

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=self.algorithms,
                audience=self.api_audience,
                issuer=f"https://{self.domain}/"
            )

            return payload

        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication service unavailable"
            )

auth0_bearer = Auth0JWTBearer()

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    # Demo mode: return demo user without authentication
    if DEMO_MODE:
        logger.info("Demo mode enabled - returning demo user")
        return {
            "sub": "demo_user_id",
            "email": "demo@mapmyclient.com",
            "name": "Demo User",
            "https://mapmyclient.com/tenant_id": 1  # Assuming demo tenant ID is 1
        }

    # Production mode: require valid JWT token
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    token = credentials.credentials
    user = await auth0_bearer.verify_token(token)
    return user

async def get_current_tenant_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> int:
    tenant_id = current_user.get("https://mapmyclient.com/tenant_id")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenant associated with this user"
        )
    return tenant_id

class TenantFilter:
    def __init__(self, tenant_id: int = Depends(get_current_tenant_id)):
        self.tenant_id = tenant_id

    def apply(self, query):
        return query.filter_by(tenant_id=self.tenant_id)