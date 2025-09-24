# MapMyClient Backend

FastAPI backend for MapMyClient - Turn LinkedIn posts into qualified opportunities.

## Architecture

This backend follows a layered architecture pattern with clear separation of concerns:

- **routers/**: Thin FastAPI route handlers (entry points only)
  - Accept HTTP requests and route to controllers
  - Handle dependency injection for auth, database sessions
  - No business logic - pure request/response handling

- **controllers/**: Business logic layer
  - Orchestrate queries and services to fulfill business operations
  - Handle business rules and validation
  - Transform between schemas and models
  - Manage transactions and error handling

- **queries/**: Data access layer
  - Encapsulate all database operations
  - Raw SQL queries or SQLAlchemy ORM operations
  - No business logic - pure data access

- **services/**: Application services
  - External integrations (AI, third-party APIs)
  - Complex business processes that span multiple entities
  - Cross-cutting concerns

- **models/**: SQLAlchemy ORM models
  - Database schema definitions
  - Relationships and constraints

- **schemas/**: Pydantic request/response schemas
  - Input validation and serialization
  - API contract definitions

- **middleware/**: Custom FastAPI middleware
  - Authentication, logging, CORS
  - Cross-cutting HTTP concerns

- **utils/**: Utility functions and helpers

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database Setup:**
   ```bash
   # Initialize Alembic
   alembic init alembic

   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"

   # Run migrations
   alembic upgrade head

   # Seed data (optional)
   python seed_data.py
   ```

4. **Run the server:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

## Key Features

- **Multi-tenant architecture** with tenant isolation
- **Auth0 JWT authentication** with automatic user creation
- **OpenAI integration** for LinkedIn post analysis and proposal generation
- **RESTful APIs** for all core entities
- **Streaming responses** for AI endpoints
- **File upload support** with tenant-specific storage

## API Endpoints

- `/api/auth/` - Authentication endpoints
- `/api/linkedin/` - LinkedIn post ingestion and management
- `/api/ai/` - AI analysis and proposal generation
- `/api/opportunities/` - Opportunity CRUD operations
- `/api/companies/` - Company management
- `/api/contacts/` - Contact management
- `/api/proposals/` - Proposal management
- `/api/campaigns/` - Campaign management
- `/api/files/` - File upload and management

## Data Model

Core entities with multi-tenant support:
- Tenant → Users, Posts, Companies, Opportunities, etc.
- LinkedInPost → Opportunities (source tracking)
- Company → Contacts, Opportunities
- Opportunity → Proposal (1:1 in MVP)

## Security

- JWT validation on all protected routes
- Tenant-scoped data access
- CORS configuration for frontend integration
- Input validation with Pydantic schemas

## Development

- Use `alembic revision --autogenerate` for database schema changes
- All queries must include tenant filtering
- Follow the existing patterns for new endpoints
- Add appropriate error handling and logging