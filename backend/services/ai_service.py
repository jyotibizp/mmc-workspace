from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from models import LinkedInPost, Opportunity
from queries.linkedin_queries import LinkedInQueries
from queries.opportunity_queries import OpportunityQueries
from database import settings
from utils.response_helpers import not_found_error
from prompts import linkedin_analysis, proposal_generation
import json
from typing import Optional, Dict, Any

class AIService:
    def __init__(self, db: Session):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.linkedin_queries = LinkedInQueries(db)
        self.opportunity_queries = OpportunityQueries(db)

    async def analyze_linkedin_post(self, post_id: int, tenant_id: int) -> Dict[str, Any]:
        # Use queries layer instead of direct DB access
        post = self.linkedin_queries.get_post_by_id(post_id, tenant_id)

        if not post:
            raise not_found_error("Post", post_id)

        prompt = linkedin_analysis.USER_PROMPT_TEMPLATE.format(
            post_content=post.content,
            author_profile_url=post.author_profile_url
        )

        try:
            response = await self.client.chat.completions.create(
                **linkedin_analysis.MODEL_CONFIG,
                messages=[
                    {"role": "system", "content": linkedin_analysis.SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt}
                ]
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")

    async def generate_proposal(
        self,
        opportunity_id: int,
        tenant_id: int,
        template_id: Optional[int] = None,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        # Use queries layer instead of direct DB access
        opportunity = self.opportunity_queries.get_opportunity_by_id(opportunity_id, tenant_id)

        if not opportunity:
            raise not_found_error("Opportunity", opportunity_id)

        prompt = proposal_generation.USER_PROMPT_TEMPLATE.format(
            title=opportunity.title,
            summary=opportunity.summary,
            tags=opportunity.tags,
            additional_context=additional_context or 'None'
        )

        try:
            response = await self.client.chat.completions.create(
                **proposal_generation.MODEL_CONFIG,
                messages=[
                    {"role": "system", "content": proposal_generation.SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.choices[0].message.content

            sections = self._parse_proposal_sections(content)

            return {
                "proposal_content": content,
                "suggested_sections": sections
            }

        except Exception as e:
            raise Exception(f"Proposal generation failed: {str(e)}")

    def _parse_proposal_sections(self, content: str) -> list:
        sections = []
        current_section = None
        current_content = []

        for line in content.split('\n'):
            if line.strip().startswith(('#', '##', '###')):
                if current_section:
                    sections.append({
                        "title": current_section,
                        "content": '\n'.join(current_content).strip()
                    })
                current_section = line.strip().lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            sections.append({
                "title": current_section,
                "content": '\n'.join(current_content).strip()
            })

        return sections