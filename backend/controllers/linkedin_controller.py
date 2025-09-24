from sqlalchemy.orm import Session
from schemas.linkedin import LinkedInPostCreate, LinkedInPostResponse
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