from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import *

def create_seed_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Create a demo tenant
        demo_tenant = Tenant(
            name="Demo Tenant",
            settings={"demo": True}
        )
        db.add(demo_tenant)
        db.flush()

        # Create a demo user
        demo_user = User(
            tenant_id=demo_tenant.id,
            auth0_user_id="demo_user_id",
            email="demo@mapmyclient.com",
            name="Demo User",
            role="admin"
        )
        db.add(demo_user)

        # Create demo companies
        companies = [
            Company(
                tenant_id=demo_tenant.id,
                name="TechCorp Solutions",
                domain="techcorp.com",
                linkedin_url="https://linkedin.com/company/techcorp"
            ),
            Company(
                tenant_id=demo_tenant.id,
                name="StartupXYZ",
                domain="startupxyz.com",
                linkedin_url="https://linkedin.com/company/startupxyz"
            )
        ]

        for company in companies:
            db.add(company)

        db.flush()

        # Create demo contacts
        contacts = [
            Contact(
                tenant_id=demo_tenant.id,
                company_id=companies[0].id,
                name="John Smith",
                email="john@techcorp.com",
                linkedin_profile_url="https://linkedin.com/in/johnsmith"
            ),
            Contact(
                tenant_id=demo_tenant.id,
                company_id=companies[1].id,
                name="Jane Doe",
                email="jane@startupxyz.com",
                linkedin_profile_url="https://linkedin.com/in/janedoe"
            )
        ]

        for contact in contacts:
            db.add(contact)

        db.commit()
        print("Seed data created successfully!")

    except Exception as e:
        print(f"Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()