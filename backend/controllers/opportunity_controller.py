from sqlalchemy.orm import Session
from schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from services.opportunity_service import OpportunityService
from queries.opportunity_queries import OpportunityQueries
from utils.response_helpers import not_found_error, deletion_success
from typing import List, Optional

class OpportunityController:
    def __init__(self, db: Session):
        self.db = db
        self.opportunity_service = OpportunityService(db)
        self.queries = OpportunityQueries(db)

    def create_opportunity(
        self,
        opportunity: OpportunityCreate,
        tenant_id: int
    ) -> OpportunityResponse:
        opportunity_data = opportunity.model_dump()
        opportunity_data["tenant_id"] = tenant_id

        # Use service for business logic and validation
        new_opportunity = self.opportunity_service.create_opportunity_with_validation(opportunity_data)
        return OpportunityResponse.model_validate(new_opportunity)

    def get_opportunities(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[OpportunityResponse]:
        opportunities = self.queries.get_opportunities_by_tenant(
            tenant_id, skip, limit, status
        )
        return [OpportunityResponse.model_validate(opp) for opp in opportunities]

    def get_opportunity(
        self,
        opportunity_id: int,
        tenant_id: int
    ) -> OpportunityResponse:
        opportunity = self.queries.get_opportunity_by_id(opportunity_id, tenant_id)

        if not opportunity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found"
            )

        return OpportunityResponse.model_validate(opportunity)

    def update_opportunity(
        self,
        opportunity_id: int,
        opportunity_update: OpportunityUpdate,
        tenant_id: int
    ) -> OpportunityResponse:
        opportunity = self.queries.get_opportunity_by_id(opportunity_id, tenant_id)

        if not opportunity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found"
            )

        update_data = opportunity_update.model_dump(exclude_unset=True)
        updated_opportunity = self.queries.update_opportunity(opportunity, update_data)

        return OpportunityResponse.model_validate(updated_opportunity)

    def delete_opportunity(
        self,
        opportunity_id: int,
        tenant_id: int
    ) -> dict:
        opportunity = self.queries.get_opportunity_by_id(opportunity_id, tenant_id)

        if not opportunity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunity not found"
            )

        self.queries.delete_opportunity(opportunity)
        return {"message": "Opportunity deleted successfully"}