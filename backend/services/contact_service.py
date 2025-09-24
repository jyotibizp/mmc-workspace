from sqlalchemy.orm import Session
from queries.contact_queries import ContactQueries
from queries.company_queries import CompanyQueries
from utils.validation import validate_email, validate_linkedin_url
from utils.response_helpers import validation_error, conflict_error, not_found_error
from typing import Dict, Any, List, Optional

class ContactService:
    """Service for contact-related business operations."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = ContactQueries(db)
        self.company_queries = CompanyQueries(db)

    def create_contact_with_validation(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create contact with business validation."""
        self._validate_contact_data(contact_data)
        self._validate_company_exists(contact_data)
        self._check_contact_uniqueness(contact_data)
        self._normalize_contact_data(contact_data)

        return self.queries.create_contact(contact_data)

    def update_contact_with_validation(self, contact: Any, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact with business validation."""
        if update_data:
            self._validate_contact_data(update_data, is_update=True)

            # Validate company exists if being updated
            if "company_id" in update_data:
                self._validate_company_exists(update_data)

            # Check uniqueness for email/LinkedIn if being updated
            self._check_contact_uniqueness_for_update(contact, update_data)
            self._normalize_contact_data(update_data)

        return self.queries.update_contact(contact, update_data)

    def search_contacts(self, tenant_id: int, search_term: str) -> List[Dict[str, Any]]:
        """Search contacts by name."""
        if len(search_term.strip()) < 2:
            raise validation_error("Search term must be at least 2 characters")

        return self.queries.search_contacts_by_name(tenant_id, search_term)

    def get_contact_statistics(self, tenant_id: int) -> Dict[str, Any]:
        """Get contact statistics for a tenant."""
        total_contacts = self.queries.count_contacts_by_tenant(tenant_id)

        # Count contacts with email/phone
        all_contacts = self.queries.get_contacts_by_tenant(tenant_id, limit=1000)
        contacts_with_email = sum(1 for c in all_contacts if c.email)
        contacts_with_phone = sum(1 for c in all_contacts if c.phone)
        contacts_with_linkedin = sum(1 for c in all_contacts if c.linkedin_profile_url)

        return {
            "total_contacts": total_contacts,
            "contacts_with_email": contacts_with_email,
            "contacts_with_phone": contacts_with_phone,
            "contacts_with_linkedin": contacts_with_linkedin,
            "completion_rate": {
                "email": round((contacts_with_email / total_contacts * 100), 2) if total_contacts > 0 else 0,
                "phone": round((contacts_with_phone / total_contacts * 100), 2) if total_contacts > 0 else 0,
                "linkedin": round((contacts_with_linkedin / total_contacts * 100), 2) if total_contacts > 0 else 0
            }
        }

    def merge_contacts(self, primary_contact_id: int, secondary_contact_id: int, tenant_id: int) -> Dict[str, Any]:
        """Merge two contacts (business logic for deduplication)."""
        primary = self.queries.get_contact_by_id(primary_contact_id, tenant_id)
        secondary = self.queries.get_contact_by_id(secondary_contact_id, tenant_id)

        if not primary or not secondary:
            raise not_found_error("Contact")

        # Merge logic: primary contact gets secondary's data if primary field is empty
        merge_data = {}
        if not primary.email and secondary.email:
            merge_data["email"] = secondary.email
        if not primary.phone and secondary.phone:
            merge_data["phone"] = secondary.phone
        if not primary.linkedin_profile_url and secondary.linkedin_profile_url:
            merge_data["linkedin_profile_url"] = secondary.linkedin_profile_url

        # Update primary contact with merged data
        if merge_data:
            updated_primary = self.queries.update_contact(primary, merge_data)
        else:
            updated_primary = primary

        # Delete secondary contact
        self.queries.delete_contact(secondary)

        return updated_primary

    def _validate_contact_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """Validate contact data according to business rules."""
        # Name validation
        name = data.get("name")
        if not is_update and not name:
            raise validation_error("Contact name is required")

        if name:
            name = name.strip()
            if len(name) < 2:
                raise validation_error("Contact name must be at least 2 characters")
            if len(name) > 100:
                raise validation_error("Contact name must be less than 100 characters")

        # Email validation
        email = data.get("email")
        if email and not validate_email(email):
            raise validation_error("Invalid email address")

        # LinkedIn URL validation
        linkedin_url = data.get("linkedin_profile_url")
        if linkedin_url and not validate_linkedin_url(str(linkedin_url)):
            raise validation_error("Invalid LinkedIn profile URL")

        # Phone validation (basic)
        phone = data.get("phone")
        if phone:
            # Remove common separators and check if numeric
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) < 10 or len(clean_phone) > 15:
                raise validation_error("Phone number must be between 10-15 digits")

        # At least one contact method required
        if not is_update:
            if not any([email, phone, linkedin_url]):
                raise validation_error("At least one contact method (email, phone, or LinkedIn) is required")

    def _normalize_contact_data(self, data: Dict[str, Any]) -> None:
        """Normalize contact data for consistency."""
        # Normalize name (trim whitespace, title case)
        if "name" in data and data["name"]:
            data["name"] = data["name"].strip().title()

        # Normalize email (lowercase)
        if "email" in data and data["email"]:
            data["email"] = data["email"].strip().lower()

        # Normalize phone (remove non-digits, add formatting)
        if "phone" in data and data["phone"]:
            clean_phone = ''.join(filter(str.isdigit, data["phone"]))
            if len(clean_phone) == 10:
                data["phone"] = f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
            else:
                data["phone"] = clean_phone

        # Normalize LinkedIn URL
        if "linkedin_profile_url" in data and data["linkedin_profile_url"]:
            url = str(data["linkedin_profile_url"]).strip()
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"
            data["linkedin_profile_url"] = url

    def _validate_company_exists(self, contact_data: Dict[str, Any]) -> None:
        """Validate that the company exists if company_id is provided."""
        company_id = contact_data.get("company_id")
        if company_id:
            tenant_id = contact_data["tenant_id"]
            company = self.company_queries.get_company_by_id(company_id, tenant_id)
            if not company:
                raise not_found_error("Company", company_id)

    def _check_contact_uniqueness(self, contact_data: Dict[str, Any]) -> None:
        """Check if contact already exists by email or LinkedIn URL."""
        tenant_id = contact_data["tenant_id"]

        # Check email uniqueness
        email = contact_data.get("email")
        if email:
            existing_contact = self.queries.get_contact_by_email(email, tenant_id)
            if existing_contact:
                raise conflict_error(f"Contact with email '{email}' already exists")

        # Check LinkedIn URL uniqueness
        linkedin_url = contact_data.get("linkedin_profile_url")
        if linkedin_url:
            existing_contact = self.queries.get_contact_by_linkedin_url(str(linkedin_url), tenant_id)
            if existing_contact:
                raise conflict_error(f"Contact with LinkedIn URL already exists")

    def _check_contact_uniqueness_for_update(self, contact: Any, update_data: Dict[str, Any]) -> None:
        """Check contact uniqueness during update (excluding current contact)."""
        tenant_id = contact.tenant_id

        # Check email uniqueness
        email = update_data.get("email")
        if email:
            existing_contact = self.queries.get_contact_by_email(email, tenant_id)
            if existing_contact and existing_contact.id != contact.id:
                raise conflict_error(f"Contact with email '{email}' already exists")

        # Check LinkedIn URL uniqueness
        linkedin_url = update_data.get("linkedin_profile_url")
        if linkedin_url:
            existing_contact = self.queries.get_contact_by_linkedin_url(str(linkedin_url), tenant_id)
            if existing_contact and existing_contact.id != contact.id:
                raise conflict_error(f"Contact with LinkedIn URL already exists")