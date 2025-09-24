from sqlalchemy.orm import Session
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from services.company_service import CompanyService
from queries.company_queries import CompanyQueries
from utils.response_helpers import not_found_error, deletion_success
from typing import List

class CompanyController:
    def __init__(self, db: Session):
        self.db = db
        self.company_service = CompanyService(db)
        self.queries = CompanyQueries(db)

    def create_company(
        self,
        company: CompanyCreate,
        tenant_id: int
    ) -> CompanyResponse:
        company_data = {
            "tenant_id": tenant_id,
            "name": company.name,
            "domain": company.domain,
            "linkedin_url": str(company.linkedin_url) if company.linkedin_url else None
        }

        # Use service for business logic and validation
        new_company = self.company_service.create_company_with_validation(company_data)
        return CompanyResponse.model_validate(new_company)

    def get_companies(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[CompanyResponse]:
        # Use queries directly for simple reads
        companies = self.queries.get_companies_by_tenant(tenant_id, skip, limit)
        return [CompanyResponse.model_validate(company) for company in companies]

    def get_company(
        self,
        company_id: int,
        tenant_id: int
    ) -> CompanyResponse:
        # Use queries directly for simple reads
        company = self.queries.get_company_by_id(company_id, tenant_id)

        if not company:
            raise not_found_error("Company", company_id)

        return CompanyResponse.model_validate(company)

    def update_company(
        self,
        company_id: int,
        company_update: CompanyUpdate,
        tenant_id: int
    ) -> CompanyResponse:
        company = self.queries.get_company_by_id(company_id, tenant_id)

        if not company:
            raise not_found_error("Company", company_id)

        update_data = company_update.model_dump(exclude_unset=True)

        # Use service for business validation
        updated_company = self.company_service.update_company_with_validation(company, update_data)

        return CompanyResponse.model_validate(updated_company)

    def delete_company(
        self,
        company_id: int,
        tenant_id: int
    ) -> dict:
        company = self.queries.get_company_by_id(company_id, tenant_id)

        if not company:
            raise not_found_error("Company", company_id)

        self.queries.delete_company(company)
        return deletion_success("Company")