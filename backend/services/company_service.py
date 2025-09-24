from sqlalchemy.orm import Session
from queries.company_queries import CompanyQueries
from utils.validation import normalize_domain, validate_linkedin_url
from utils.response_helpers import validation_error
from typing import Dict, Any, List

class CompanyService:
    """Service for company-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = CompanyQueries(db)

    def create_company_with_validation(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create company with business validation and data normalization."""
        self._validate_company_data(company_data)
        self._normalize_company_data(company_data)

        # Check for duplicates by normalized domain or name
        self._check_company_uniqueness(company_data)

        return self.queries.create_company(company_data)

    def update_company_with_validation(self, company: Any, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update company with business validation."""
        if update_data:
            self._validate_company_data(update_data, is_update=True)
            self._normalize_company_data(update_data)

        return self.queries.update_company(company, update_data)

    def get_companies_by_domain(self, tenant_id: int, domain: str) -> List[Dict[str, Any]]:
        """Get companies by normalized domain."""
        normalized_domain = normalize_domain(domain)
        return self.queries.get_companies_by_tenant(tenant_id, domain_filter=normalized_domain)

    def _validate_company_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """Validate company data according to business rules."""
        # Name validation
        name = data.get("name")
        if not is_update and not name:
            raise validation_error("Company name is required")

        if name and len(name.strip()) < 2:
            raise validation_error("Company name must be at least 2 characters")

        # LinkedIn URL validation
        linkedin_url = data.get("linkedin_url")
        if linkedin_url and not validate_linkedin_url(str(linkedin_url)):
            raise validation_error("Invalid LinkedIn company URL")

        # Domain validation
        domain = data.get("domain")
        if domain:
            normalized = normalize_domain(domain)
            if not normalized or len(normalized) < 3:
                raise validation_error("Invalid company domain")

    def _normalize_company_data(self, data: Dict[str, Any]) -> None:
        """Normalize company data for consistency."""
        # Normalize domain
        if "domain" in data and data["domain"]:
            data["domain"] = normalize_domain(data["domain"])

        # Normalize name (trim whitespace, title case)
        if "name" in data and data["name"]:
            data["name"] = data["name"].strip()

        # Ensure LinkedIn URL format
        if "linkedin_url" in data and data["linkedin_url"]:
            url = str(data["linkedin_url"]).strip()
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
            data["linkedin_url"] = url

    def _check_company_uniqueness(self, company_data: Dict[str, Any]) -> None:
        """Check if company already exists by domain or similar name."""
        tenant_id = company_data["tenant_id"]

        # Check by domain if provided
        domain = company_data.get("domain")
        if domain:
            existing_companies = self.queries.get_companies_by_tenant(tenant_id)
            for company in existing_companies:
                if company.domain and normalize_domain(company.domain) == normalize_domain(domain):
                    raise validation_error(f"Company with domain '{domain}' already exists")

        # Check by similar name
        name = company_data.get("name", "").lower().strip()
        if name:
            existing_companies = self.queries.get_companies_by_tenant(tenant_id)
            for company in existing_companies:
                if company.name and company.name.lower().strip() == name:
                    raise validation_error(f"Company with name '{company_data['name']}' already exists")