from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from models import LinkedInPost, Opportunity
from queries.linkedin_queries import LinkedInQueries
from queries.opportunity_queries import OpportunityQueries
from database import settings
from utils.response_helpers import not_found_error
from prompts import linkedin_analysis, proposal_generation, opportunity_analysis
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

    async def analyze_opportunity_comprehensive(self, post, enable_cache: bool = True) -> Dict[str, Any]:
        """Comprehensive AI analysis of LinkedIn post for opportunity detection."""

        # Use prompt from prompts layer
        prompt = opportunity_analysis.USER_PROMPT_TEMPLATE.format(
            post_content=post.content,
            author_profile_url=post.author_profile_url or 'Not provided'
        )

        try:
            response = await self.client.chat.completions.create(
                **opportunity_analysis.MODEL_CONFIG,
                messages=[
                    {"role": "system", "content": opportunity_analysis.SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt}
                ]
            )

            result = json.loads(response.choices[0].message.content)

            # Helper function to extract value from nested format
            def extract_value(field, default=None):
                if isinstance(field, dict) and 'value' in field:
                    return field['value'] if field['value'] not in ['Not mentioned', 'Not provided', None] else default
                return field if field not in ['Not mentioned', 'Not provided', None] else default

            def extract_confidence(field, default=0.0):
                if isinstance(field, dict) and 'confidence' in field:
                    return field['confidence']
                return default

            # Process company suggestion
            company_raw = result.get("company_suggestion")
            company_suggestion = None
            if company_raw and extract_value(company_raw.get('name')):
                company_suggestion = {
                    "name": extract_value(company_raw.get('name')),
                    "confidence": extract_confidence(company_raw.get('name'), 0.0),
                    "domain": extract_value(company_raw.get('domain')),
                    "linkedin_url": extract_value(company_raw.get('linkedin_url'))
                }

            # Process contact suggestion
            contact_raw = result.get("contact_suggestion")
            contact_suggestion = None
            if contact_raw:
                contact_suggestion = {
                    "name": extract_value(contact_raw.get('name')),
                    "email": extract_value(contact_raw.get('email')),
                    "phone": extract_value(contact_raw.get('phone')),
                    "linkedin_profile_url": extract_value(contact_raw.get('linkedin_profile_url')),
                    "confidence": max([
                        extract_confidence(contact_raw.get('name'), 0.0),
                        extract_confidence(contact_raw.get('email'), 0.0),
                        extract_confidence(contact_raw.get('phone'), 0.0),
                        extract_confidence(contact_raw.get('linkedin_profile_url'), 0.0)
                    ])
                }

            # Ensure all required fields exist with defaults
            return {
                "is_opportunity": result.get("is_opportunity", False),
                "confidence": result.get("confidence", 0.0),
                "extracted_fields": result.get("extracted_fields", {}),
                "company_suggestion": company_suggestion,
                "contact_suggestion": contact_suggestion,
                "category": result.get("category", "other"),
                "urgency": result.get("urgency", "normal"),
                "tags": result.get("tags", []),
                "budget_range": extract_value(result.get("budget_range")),
                "timeline": extract_value(result.get("timeline"))
            }

        except json.JSONDecodeError as e:
            raise Exception(f"AI returned invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")

    async def analyze_opportunity_comprehensive_streaming(self, post, enable_cache: bool = True):
        """Streaming version of comprehensive AI analysis with progressive updates."""

        # Yield initial status
        yield json.dumps({"status": "starting", "message": "Initializing AI analysis..."}) + "\n"

        # Use prompt from prompts layer
        prompt = opportunity_analysis.USER_PROMPT_TEMPLATE.format(
            post_content=post.content,
            author_profile_url=post.author_profile_url or 'Not provided'
        )

        yield json.dumps({"status": "analyzing", "message": "Analyzing post content with AI..."}) + "\n"

        try:
            response = await self.client.chat.completions.create(
                **opportunity_analysis.MODEL_CONFIG,
                messages=[
                    {"role": "system", "content": opportunity_analysis.SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt}
                ]
            )

            yield json.dumps({"status": "processing", "message": "Processing AI response..."}) + "\n"

            result = json.loads(response.choices[0].message.content)

            # Helper functions (same as non-streaming version)
            def extract_value(field, default=None):
                if isinstance(field, dict) and 'value' in field:
                    return field['value'] if field['value'] not in ['Not mentioned', 'Not provided', None] else default
                return field if field not in ['Not mentioned', 'Not provided', None] else default

            def extract_confidence(field, default=0.0):
                if isinstance(field, dict) and 'confidence' in field:
                    return field['confidence']
                return default

            # Stream progress updates for different analysis phases
            yield json.dumps({"status": "extracting_fields", "message": "Extracting opportunity fields..."}) + "\n"

            # Process company suggestion
            company_raw = result.get("company_suggestion")
            company_suggestion = None
            if company_raw and extract_value(company_raw.get('name')):
                company_suggestion = {
                    "name": extract_value(company_raw.get('name')),
                    "confidence": extract_confidence(company_raw.get('name'), 0.0),
                    "domain": extract_value(company_raw.get('domain')),
                    "linkedin_url": extract_value(company_raw.get('linkedin_url'))
                }
                yield json.dumps({"status": "company_extracted", "message": f"Found company: {company_suggestion['name']}"}) + "\n"

            # Process contact suggestion
            contact_raw = result.get("contact_suggestion")
            contact_suggestion = None
            if contact_raw:
                contact_suggestion = {
                    "name": extract_value(contact_raw.get('name')),
                    "email": extract_value(contact_raw.get('email')),
                    "phone": extract_value(contact_raw.get('phone')),
                    "linkedin_profile_url": extract_value(contact_raw.get('linkedin_profile_url')),
                    "confidence": max([
                        extract_confidence(contact_raw.get('name'), 0.0),
                        extract_confidence(contact_raw.get('email'), 0.0),
                        extract_confidence(contact_raw.get('phone'), 0.0),
                        extract_confidence(contact_raw.get('linkedin_profile_url'), 0.0)
                    ])
                }
                yield json.dumps({"status": "contact_extracted", "message": f"Found contact info"}) + "\n"

            yield json.dumps({"status": "finalizing", "message": "Finalizing analysis results..."}) + "\n"

            # Final result
            final_result = {
                "is_opportunity": result.get("is_opportunity", False),
                "confidence": result.get("confidence", 0.0),
                "extracted_fields": result.get("extracted_fields", {}),
                "company_suggestion": company_suggestion,
                "contact_suggestion": contact_suggestion,
                "category": result.get("category", "other"),
                "urgency": result.get("urgency", "normal"),
                "tags": result.get("tags", []),
                "budget_range": extract_value(result.get("budget_range")),
                "timeline": extract_value(result.get("timeline"))
            }

            # Yield final result
            yield json.dumps({"status": "completed", "result": final_result}) + "\n"

        except json.JSONDecodeError as e:
            yield json.dumps({"status": "error", "error": f"AI returned invalid JSON: {str(e)}"}) + "\n"
        except Exception as e:
            yield json.dumps({"status": "error", "error": f"AI analysis failed: {str(e)}"}) + "\n"