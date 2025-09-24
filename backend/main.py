from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from database import settings

from routers import (
    auth,
    linkedin,
    ai,
    opportunities,
    companies,
    contacts,
    proposals,
    campaigns,
    files
)

logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MapMyClient API",
    description="API for MapMyClient - Turn LinkedIn posts into qualified opportunities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(linkedin.router, prefix="/api/linkedin", tags=["LinkedIn"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(opportunities.router, prefix="/api/opportunities", tags=["Opportunities"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(proposals.router, prefix="/api/proposals", tags=["Proposals"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])

@app.get("/")
async def root():
    return {"message": "MapMyClient API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.environment == "development")