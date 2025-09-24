from sqlalchemy.orm import Session
from queries.linkedin_queries import LinkedInQueries
from utils.validation import validate_linkedin_url
from utils.response_helpers import conflict_error, validation_error
from typing import Dict, Any

class LinkedInService:
    """Service for LinkedIn-specific business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.queries = LinkedInQueries(db)

    def validate_post_data(self, post_data: Dict[str, Any]) -> None:
        """Validate LinkedIn post data before processing."""
        post_url = str(post_data.get("post_url", ""))

        if not validate_linkedin_url(post_url):
            raise validation_error("Invalid LinkedIn post URL")

        author_url = post_data.get("author_profile_url")
        if author_url and not validate_linkedin_url(str(author_url)):
            raise validation_error("Invalid LinkedIn author profile URL")

    def check_post_exists(self, post_url: str, tenant_id: int) -> None:
        """Check if a post already exists for this tenant."""
        existing_post = self.queries.get_post_by_url(post_url, tenant_id)
        if existing_post:
            raise conflict_error("Post already exists")

    def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new LinkedIn post with validation."""
        self.validate_post_data(post_data)
        self.check_post_exists(post_data["post_url"], post_data["tenant_id"])

        return self.queries.create_linkedin_post(post_data)