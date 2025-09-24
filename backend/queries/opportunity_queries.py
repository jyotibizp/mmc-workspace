from sqlalchemy.orm import Session
from models import Opportunity
from typing import Optional, List

class OpportunityQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_opportunity(self, opportunity_data: dict) -> Opportunity:
        new_opportunity = Opportunity(**opportunity_data)
        self.db.add(new_opportunity)
        self.db.commit()
        self.db.refresh(new_opportunity)
        return new_opportunity

    def get_opportunities_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Opportunity]:
        query = self.db.query(Opportunity).filter(Opportunity.tenant_id == tenant_id)

        if status:
            query = query.filter(Opportunity.status == status)

        return query.offset(skip).limit(limit).all()

    def get_opportunity_by_id(self, opportunity_id: int, tenant_id: int) -> Optional[Opportunity]:
        return self.db.query(Opportunity).filter(
            Opportunity.id == opportunity_id,
            Opportunity.tenant_id == tenant_id
        ).first()

    def update_opportunity(self, opportunity: Opportunity, update_data: dict) -> Opportunity:
        for field, value in update_data.items():
            setattr(opportunity, field, value)
        self.db.commit()
        self.db.refresh(opportunity)
        return opportunity

    def delete_opportunity(self, opportunity: Opportunity) -> None:
        self.db.delete(opportunity)
        self.db.commit()