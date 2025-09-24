from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from queries.linkedin_queries import LinkedInQueries
from utils.validation import validate_linkedin_url
from utils.response_helpers import conflict_error, validation_error
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

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

    def create_posts_batch(self, posts_data: List[Dict[str, Any]], tenant_id: int, user_id: int) -> Dict[str, Any]:
        """Create multiple LinkedIn posts in batch with individual error handling."""
        results = []
        successful = 0
        duplicates = 0
        failed = 0

        for post_data in posts_data:
            post_url = str(post_data.get("post_url", ""))

            try:
                # Add tenant_id and user_id to each post
                post_dict = {
                    "tenant_id": tenant_id,
                    "user_id": user_id,
                    "post_url": post_url,
                    "author_profile_url": str(post_data.get("author_profile_url")) if post_data.get("author_profile_url") else None,
                    "content": post_data.get("content", ""),
                    "scraped_at": post_data.get("scraped_at")
                }

                # Validate post data
                self.validate_post_data(post_dict)

                # Check if post already exists
                existing_post = self.queries.get_post_by_url(post_url, tenant_id)
                if existing_post:
                    results.append({
                        "post_url": post_url,
                        "status": "duplicate",
                        "post_id": existing_post.id,
                        "error": None
                    })
                    duplicates += 1
                    continue

                # Create the post
                new_post = self.queries.create_linkedin_post(post_dict)
                results.append({
                    "post_url": post_url,
                    "status": "success",
                    "post_id": new_post.id,
                    "error": None
                })
                successful += 1

            except IntegrityError as e:
                # Handle database constraint violations (e.g., duplicate key)
                self.db.rollback()
                logger.warning(f"Database integrity error for post {post_url}: {e}")
                results.append({
                    "post_url": post_url,
                    "status": "duplicate",
                    "post_id": None,
                    "error": "Post already exists"
                })
                duplicates += 1

            except Exception as e:
                logger.error(f"Failed to create post {post_url}: {e}")
                results.append({
                    "post_url": post_url,
                    "status": "failed",
                    "post_id": None,
                    "error": str(e)
                })
                failed += 1

        return {
            "total": len(posts_data),
            "successful": successful,
            "duplicates": duplicates,
            "failed": failed,
            "results": results
        }