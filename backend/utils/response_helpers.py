from fastapi import HTTPException, status
from typing import Optional, Any

def not_found_error(entity: str, entity_id: Optional[Any] = None) -> HTTPException:
    """Generate a standardized 404 error."""
    detail = f"{entity} not found"
    if entity_id:
        detail = f"{entity} with id {entity_id} not found"

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )

def conflict_error(message: str) -> HTTPException:
    """Generate a standardized 409 conflict error."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )

def validation_error(message: str) -> HTTPException:
    """Generate a standardized 422 validation error."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=message
    )

def success_message(action: str, entity: str) -> dict:
    """Generate a standardized success message."""
    return {"message": f"{entity} {action} successfully"}

def deletion_success(entity: str) -> dict:
    """Generate a standardized deletion success message."""
    return success_message("deleted", entity)