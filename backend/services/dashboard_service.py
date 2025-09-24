from sqlalchemy.orm import Session
from queries.opportunity_queries import OpportunityQueries
from queries.proposal_queries import ProposalQueries
from queries.campaign_queries import CampaignQueries
from queries.linkedin_queries import LinkedInQueries
from datetime import datetime, timedelta
from typing import Dict, Any, List

class DashboardService:
    """Service for dashboard-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.opportunity_queries = OpportunityQueries(db)
        self.proposal_queries = ProposalQueries(db)
        self.campaign_queries = CampaignQueries(db)
        self.linkedin_queries = LinkedInQueries(db)

    def _get_date_filter(self, date_range: str) -> datetime:
        """Convert date range string to datetime filter."""
        days_map = {"7d": 7, "30d": 30, "90d": 90}
        days = days_map.get(date_range, 30)
        return datetime.now() - timedelta(days=days)

    def get_dashboard_statistics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get comprehensive dashboard statistics with business logic."""
        from_date = self._get_date_filter(date_range)

        # Get counts from different entities using available methods
        opportunities = self.opportunity_queries.get_opportunities_by_tenant(tenant_id)
        opportunities_count = len(opportunities)

        proposals_count = self.proposal_queries.count_proposals_by_tenant(tenant_id)
        campaigns_count = self.campaign_queries.count_campaigns_by_tenant(tenant_id)

        # Get posts count - check if method exists, otherwise default to 0
        try:
            posts_count = self.linkedin_queries.count_posts_by_tenant(tenant_id)
        except AttributeError:
            posts_count = 0

        # Get status counts for opportunities with business logic (already fetched above)
        status_counts = self._calculate_opportunity_status_counts(opportunities)

        return {
            "opportunities_count": opportunities_count,
            "proposals_count": proposals_count,
            "campaigns_count": campaigns_count,
            "posts_count": posts_count,
            "status_counts": status_counts,
            "date_range": date_range
        }

    def get_opportunities_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get opportunities analytics with business intelligence."""
        opportunities = self.opportunity_queries.get_opportunities_by_tenant(tenant_id)

        # Apply business logic for status analysis
        status_counts = self._calculate_opportunity_status_counts(opportunities)
        conversion_rate = self._calculate_conversion_rate(opportunities)

        return {
            "total_count": len(opportunities),
            "status_counts": status_counts,
            "conversion_rate": conversion_rate,
            "date_range": date_range
        }

    def get_proposals_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get proposals analytics with business intelligence."""
        proposals = self.proposal_queries.get_proposals_by_tenant(tenant_id)

        # Apply business logic for proposal analysis
        status_counts = self._calculate_proposal_status_counts(proposals)
        active_count = self._calculate_active_proposals_count(status_counts)

        return {
            "total_count": len(proposals),
            "status_counts": status_counts,
            "active_count": active_count,
            "date_range": date_range
        }

    def get_campaigns_analytics(self, tenant_id: int, date_range: str = "30d") -> Dict[str, Any]:
        """Get campaigns analytics with business intelligence."""
        campaigns = self.campaign_queries.get_campaigns_by_tenant(tenant_id)

        # Apply business logic for campaign analysis
        active_count = self._calculate_active_campaigns_count(campaigns)

        return {
            "total_count": len(campaigns),
            "active_count": active_count,
            "archived_count": len(campaigns) - active_count,
            "date_range": date_range
        }

    def get_recent_activity(self, tenant_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent activity timeline with business logic."""
        # Get recent data with optimized queries
        recent_opportunities = self.opportunity_queries.get_opportunities_by_tenant(tenant_id, limit=limit//2)
        recent_proposals = self.proposal_queries.get_proposals_by_tenant(tenant_id, limit=limit//2)

        activities = []

        # Transform opportunities with business logic
        for opp in recent_opportunities:
            activities.append(self._create_activity_item("opportunity", opp))

        # Transform proposals with business logic
        for proposal in recent_proposals:
            activities.append(self._create_activity_item("proposal", proposal))

        # Sort and limit with business rules
        activities.sort(key=lambda x: x["created_at"], reverse=True)
        return activities[:limit]

    def get_dashboard_overview(self, tenant_id: int) -> Dict[str, Any]:
        """Get complete dashboard overview with comprehensive business intelligence."""
        stats = self.get_dashboard_statistics(tenant_id)
        recent_activity = self.get_recent_activity(tenant_id, 5)

        # Get recent opportunities with business formatting
        recent_opportunities = self.opportunity_queries.get_opportunities_by_tenant(tenant_id, limit=8)
        formatted_opportunities = [
            self._format_opportunity_for_dashboard(opp) for opp in recent_opportunities
        ]

        return {
            "statistics": stats,
            "recent_activity": recent_activity,
            "recent_opportunities": formatted_opportunities
        }

    # Private helper methods for business logic
    def _calculate_opportunity_status_counts(self, opportunities) -> Dict[str, int]:
        """Calculate opportunity status counts with business rules."""
        status_counts = {}
        for opp in opportunities:
            status = opp.status or 'draft'  # Business rule: default to draft
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts

    def _calculate_conversion_rate(self, opportunities) -> float:
        """Calculate conversion rate with business logic."""
        if not opportunities:
            return 0.0

        won_count = sum(1 for opp in opportunities if opp.status == 'won')
        return (won_count / len(opportunities)) * 100

    def _calculate_proposal_status_counts(self, proposals) -> Dict[str, int]:
        """Calculate proposal status counts with business rules."""
        status_counts = {}
        for proposal in proposals:
            status = proposal.status or 'draft'  # Business rule: default to draft
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts

    def _calculate_active_proposals_count(self, status_counts: Dict[str, int]) -> int:
        """Calculate active proposals count with business logic."""
        return status_counts.get('active', 0) + status_counts.get('sent', 0)

    def _calculate_active_campaigns_count(self, campaigns) -> int:
        """Calculate active campaigns count with business logic."""
        active_count = 0
        for campaign in campaigns:
            # Business rule: campaign is active if not archived
            if not hasattr(campaign, 'archived') or not campaign.archived:
                active_count += 1
        return active_count

    def _create_activity_item(self, item_type: str, item) -> Dict[str, Any]:
        """Create activity item with business formatting."""
        if item_type == "opportunity":
            return {
                "type": "opportunity",
                "description": f"New opportunity: {item.title}",
                "created_at": item.created_at,
                "entity_id": item.id
            }
        elif item_type == "proposal":
            return {
                "type": "proposal",
                "description": f"Proposal created: {item.title}",
                "created_at": item.created_at,
                "entity_id": item.id
            }

    def _format_opportunity_for_dashboard(self, opp) -> Dict[str, Any]:
        """Format opportunity for dashboard with business rules."""
        return {
            "id": opp.id,
            "title": opp.title,
            "status": opp.status or 'draft',  # Business rule: default status
            "company_name": opp.company_name,
            "budget_range": opp.budget_range,
            "created_at": opp.created_at
        }