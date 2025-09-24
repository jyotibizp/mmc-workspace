from sqlalchemy.orm import Session
from models import Company
from typing import Optional, List

class CompanyQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_company(self, company_data: dict) -> Company:
        new_company = Company(**company_data)
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company

    def get_companies_by_tenant(self, tenant_id: int, skip: int = 0, limit: int = 100, domain_filter: Optional[str] = None) -> List[Company]:
        query = self.db.query(Company).filter(Company.tenant_id == tenant_id)

        if domain_filter:
            query = query.filter(Company.domain == domain_filter)

        return query.offset(skip).limit(limit).all()

    def get_company_by_id(self, company_id: int, tenant_id: int) -> Optional[Company]:
        return self.db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()

    def update_company(self, company: Company, update_data: dict) -> Company:
        for field, value in update_data.items():
            if field == "linkedin_url" and value:
                value = str(value)
            setattr(company, field, value)
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete_company(self, company: Company) -> None:
        self.db.delete(company)
        self.db.commit()