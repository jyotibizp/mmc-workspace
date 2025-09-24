from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mapmyclient")
    auth0_domain: str = os.getenv("AUTH0_DOMAIN", "")
    auth0_api_audience: str = os.getenv("AUTH0_API_AUDIENCE", "")
    auth0_algorithms: str = os.getenv("AUTH0_ALGORITHMS", "RS256")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    demo_mode: str = os.getenv("DEMO_MODE", "false")

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=settings.environment == "development"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()