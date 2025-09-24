from sqlalchemy.orm import Session
from schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from services.contact_service import ContactService
from queries.contact_queries import ContactQueries
from utils.response_helpers import not_found_error, deletion_success
from typing import List, Optional

class ContactController:
    def __init__(self, db: Session):
        self.db = db
        self.contact_service = ContactService(db)
        self.queries = ContactQueries(db)

    def create_contact(
        self,
        contact: ContactCreate,
        tenant_id: int
    ) -> ContactResponse:
        """Create a new contact."""
        contact_data = {
            "tenant_id": tenant_id,
            "company_id": contact.company_id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "linkedin_profile_url": str(contact.linkedin_profile_url) if contact.linkedin_profile_url else None
        }

        # Use service for business logic and validation
        new_contact = self.contact_service.create_contact_with_validation(contact_data)
        return ContactResponse.model_validate(new_contact)

    def get_contacts(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        company_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[ContactResponse]:
        """Get contacts with optional filters."""
        if search:
            # Use service for business logic
            contacts = self.contact_service.search_contacts(tenant_id, search)
        else:
            # Use queries directly for simple reads
            contacts = self.queries.get_contacts_by_tenant(tenant_id, skip, limit, company_id)

        return [ContactResponse.model_validate(contact) for contact in contacts]

    def get_contact(
        self,
        contact_id: int,
        tenant_id: int
    ) -> ContactResponse:
        """Get a specific contact."""
        # Use queries directly for simple reads
        contact = self.queries.get_contact_by_id(contact_id, tenant_id)

        if not contact:
            raise not_found_error("Contact", contact_id)

        return ContactResponse.model_validate(contact)

    def update_contact(
        self,
        contact_id: int,
        contact_update: ContactUpdate,
        tenant_id: int
    ) -> ContactResponse:
        """Update an existing contact."""
        contact = self.queries.get_contact_by_id(contact_id, tenant_id)

        if not contact:
            raise not_found_error("Contact", contact_id)

        update_data = contact_update.model_dump(exclude_unset=True)

        # Use service for business validation
        updated_contact = self.contact_service.update_contact_with_validation(contact, update_data)

        return ContactResponse.model_validate(updated_contact)

    def delete_contact(
        self,
        contact_id: int,
        tenant_id: int
    ) -> dict:
        """Delete a contact."""
        contact = self.queries.get_contact_by_id(contact_id, tenant_id)

        if not contact:
            raise not_found_error("Contact", contact_id)

        self.queries.delete_contact(contact)
        return deletion_success("Contact")

    def get_contact_statistics(
        self,
        tenant_id: int
    ) -> dict:
        """Get contact statistics for tenant."""
        # Use service for business logic
        return self.contact_service.get_contact_statistics(tenant_id)

    def get_contacts_by_company(
        self,
        company_id: int,
        tenant_id: int
    ) -> List[ContactResponse]:
        """Get all contacts for a specific company."""
        # Use queries directly for simple reads
        contacts = self.queries.get_contacts_by_company(company_id, tenant_id)
        return [ContactResponse.model_validate(contact) for contact in contacts]

    def merge_contacts(
        self,
        primary_contact_id: int,
        secondary_contact_id: int,
        tenant_id: int
    ) -> ContactResponse:
        """Merge two contacts (deduplication)."""
        # Use service for business logic
        merged_contact = self.contact_service.merge_contacts(
            primary_contact_id, secondary_contact_id, tenant_id
        )
        return ContactResponse.model_validate(merged_contact)