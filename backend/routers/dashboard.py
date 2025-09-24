from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth import get_current_tenant_id
from controllers.dashboard_controller import DashboardController
from typing import Optional

router = APIRouter()

@router.get("/statistics")
async def get_dashboard_statistics(
    date_range: str = Query("30d", description="Date range: 7d, 30d, 90d"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard statistics."""
    controller = DashboardController(db)
    return controller.get_dashboard_statistics(tenant_id, date_range)

@router.get("/analytics/opportunities")
async def get_opportunities_analytics(
    date_range: str = Query("30d", description="Date range: 7d, 30d, 90d"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get opportunities analytics with trends."""
    controller = DashboardController(db)
    return controller.get_opportunities_analytics(tenant_id, date_range)

@router.get("/analytics/proposals")
async def get_proposals_analytics(
    date_range: str = Query("30d", description="Date range: 7d, 30d, 90d"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get proposals analytics with conversion rates."""
    controller = DashboardController(db)
    return controller.get_proposals_analytics(tenant_id, date_range)

@router.get("/analytics/campaigns")
async def get_campaigns_analytics(
    date_range: str = Query("30d", description="Date range: 7d, 30d, 90d"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get campaigns analytics with performance metrics."""
    controller = DashboardController(db)
    return controller.get_campaigns_analytics(tenant_id, date_range)

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = Query(10, description="Number of activities to return"),
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get recent activity timeline."""
    controller = DashboardController(db)
    return controller.get_recent_activity(tenant_id, limit)

@router.get("/overview")
async def get_dashboard_overview(
    tenant_id: int = Depends(get_current_tenant_id),
    db: Session = Depends(get_db)
):
    """Get complete dashboard overview with all metrics."""
    controller = DashboardController(db)
    return controller.get_dashboard_overview(tenant_id)