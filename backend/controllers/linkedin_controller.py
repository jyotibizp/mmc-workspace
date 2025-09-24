from sqlalchemy.orm import Session
from schemas.linkedin import LinkedInPostCreate, LinkedInPostResponse, LinkedInPostBatchCreate, BatchIngestionResponse
from services.linkedin_service import LinkedInService
from services.user_service import UserService
from queries.linkedin_queries import LinkedInQueries
from typing import List, Dict, Any

class LinkedInController:
    def __init__(self, db: Session):
        self.db = db
        self.linkedin_service = LinkedInService(db)
        self.user_service = UserService(db)
        self.queries = LinkedInQueries(db)

    def ingest_linkedin_post(
        self,
        post_data: LinkedInPostCreate,
        current_user: Dict[str, Any],
        tenant_id: int
    ) -> LinkedInPostResponse:
        # Validate user access using service
        user = self.user_service.validate_user_access(current_user, tenant_id)

        # Prepare post data
        post_dict = {
            "tenant_id": tenant_id,
            "user_id": user.id,
            "post_url": str(post_data.post_url),
            "author_profile_url": str(post_data.author_profile_url) if post_data.author_profile_url else None,
            "content": post_data.content,
            "scraped_at": post_data.scraped_at
        }

        # Create post using service (includes validation)
        new_post = self.linkedin_service.create_post(post_dict)
        return LinkedInPostResponse.model_validate(new_post)

    def get_linkedin_posts(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[LinkedInPostResponse]:
        # Use queries layer directly for simple reads
        posts = self.queries.get_posts_by_tenant(tenant_id, skip, limit)
        return [LinkedInPostResponse.model_validate(post) for post in posts]

    def get_linkedin_post(
        self,
        post_id: int,
        tenant_id: int
    ) -> LinkedInPostResponse:
        # Use queries layer directly for simple reads
        post = self.queries.get_post_by_id(post_id, tenant_id)

        if not post:
            from utils.response_helpers import not_found_error
            raise not_found_error("Post", post_id)

        return LinkedInPostResponse.model_validate(post)

    def ingest_linkedin_posts_batch(
        self,
        batch_data: LinkedInPostBatchCreate,
        current_user: Dict[str, Any],
        tenant_id: int
    ) -> BatchIngestionResponse:
        """Ingest multiple LinkedIn posts in batch."""
        # Validate user access
        user = self.user_service.validate_user_access(current_user, tenant_id)

        # Validate batch size (limit to 50 posts per batch)
        if len(batch_data.posts) > 50:
            from utils.response_helpers import validation_error
            raise validation_error("Batch size cannot exceed 50 posts")

        # Convert posts to dict format for service
        posts_data = []
        for post in batch_data.posts:
            posts_data.append({
                "post_url": str(post.post_url),
                "author_profile_url": str(post.author_profile_url) if post.author_profile_url else None,
                "content": post.content,
                "scraped_at": post.scraped_at
            })

        # Process batch using service
        result = self.linkedin_service.create_posts_batch(posts_data, tenant_id, user.id)

        return BatchIngestionResponse.model_validate(result)