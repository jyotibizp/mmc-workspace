from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_user
from controllers.auth_controller import AuthController
from typing import Dict, Any

router = APIRouter()

@router.get("/me")
async def get_me(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = AuthController(db)
    return controller.get_me(current_user)

@router.post("/authenticate")
async def authenticate(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = AuthController(db)
    return controller.authenticate_user(current_user)

@router.post("/logout")
async def logout():
    controller = AuthController(db=None)  # No DB needed for logout
    return controller.logout()

@router.get("/validate-access/{tenant_id}")
async def validate_access(
    tenant_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    controller = AuthController(db)
    return controller.validate_access(current_user, tenant_id)