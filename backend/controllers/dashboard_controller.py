from sqlalchemy.orm import Session
from services.dashboard_service import DashboardService
from typing import Dict, Any, List

class DashboardController:
    def __init__(self, db: Session):
        self.db = db
        self.service = DashboardService(db)

    def get_dashboard_statistics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get comprehensive dashboard statistics."""
        return self.service.get_dashboard_statistics(tenant_id, date_range)

    def get_opportunities_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get opportunities analytics with trends."""
        return self.service.get_opportunities_analytics(tenant_id, date_range)

    def get_proposals_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get proposals analytics with conversion rates."""
        return self.service.get_proposals_analytics(tenant_id, date_range)

    def get_campaigns_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get campaigns analytics with performance metrics."""
        return self.service.get_campaigns_analytics(tenant_id, date_range)

    def get_recent_activity(self, tenant_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activity timeline."""
        return self.service.get_recent_activity(tenant_id, limit)

    def get_dashboard_overview(self, tenant_id: int) -> Dict[str, Any]:
        """Get complete dashboard overview with all metrics."""
        return self.service.get_dashboard_overview(tenant_id)