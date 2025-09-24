from sqlalchemy.orm import Session
from models import Contact
from typing import Optional, List

class ContactQueries:
    def __init__(self, db: Session):
        self.db = db

    def create_contact(self, contact_data: dict) -> Contact:
        """Create a new contact."""
        new_contact = Contact(**contact_data)
        self.db.add(new_contact)
        self.db.commit()
        self.db.refresh(new_contact)
        return new_contact

    def get_contacts_by_tenant(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        company_id: Optional[int] = None
    ) -> List[Contact]:
        """Get contacts for a specific tenant with optional company filter."""
        query = self.db.query(Contact).filter(Contact.tenant_id == tenant_id)

        if company_id:
            query = query.filter(Contact.company_id == company_id)

        return query.offset(skip).limit(limit).all()

    def get_contact_by_id(self, contact_id: int, tenant_id: int) -> Optional[Contact]:
        """Get a specific contact by ID within tenant."""
        return self.db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.tenant_id == tenant_id
        ).first()

    def get_contact_by_email(self, email: str, tenant_id: int) -> Optional[Contact]:
        """Get contact by email within tenant."""
        return self.db.query(Contact).filter(
            Contact.email == email,
            Contact.tenant_id == tenant_id
        ).first()

    def get_contact_by_linkedin_url(self, linkedin_url: str, tenant_id: int) -> Optional[Contact]:
        """Get contact by LinkedIn URL within tenant."""
        return self.db.query(Contact).filter(
            Contact.linkedin_profile_url == linkedin_url,
            Contact.tenant_id == tenant_id
        ).first()

    def search_contacts_by_name(self, tenant_id: int, name_search: str) -> List[Contact]:
        """Search contacts by name."""
        return self.db.query(Contact).filter(
            Contact.tenant_id == tenant_id,
            Contact.name.ilike(f"%{name_search}%")
        ).all()

    def update_contact(self, contact: Contact, update_data: dict) -> Contact:
        """Update an existing contact."""
        for field, value in update_data.items():
            if field == "linkedin_profile_url" and value:
                value = str(value)
            setattr(contact, field, value)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete_contact(self, contact: Contact) -> None:
        """Delete a contact."""
        self.db.delete(contact)
        self.db.commit()

    def count_contacts_by_tenant(self, tenant_id: int) -> int:
        """Count total contacts for a tenant."""
        return self.db.query(Contact).filter(
            Contact.tenant_id == tenant_id
        ).count()

    def get_contacts_by_company(self, company_id: int, tenant_id: int) -> List[Contact]:
        """Get all contacts for a specific company."""
        return self.db.query(Contact).filter(
            Contact.company_id == company_id,
            Contact.tenant_id == tenant_id
        ).all()