from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from services.ai_service import AIService
from schemas.ai import AnalyzeExtractRequest, ProposalGenerationRequest, AnalyzeOpportunityRequest, AnalyzeOpportunityResponse
from queries.linkedin_queries import LinkedInQueries
from utils.response_helpers import not_found_error
import json

class AIController:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService(db)
        self.linkedin_queries = LinkedInQueries(db)

    async def analyze_extract_post(self, request: AnalyzeExtractRequest, tenant_id: int):
        """Analyze LinkedIn post using AI service."""
        try:
            result = await self.ai_service.analyze_linkedin_post(request.post_id, tenant_id)

            async def generate():
                yield json.dumps(result) + "\n"

            return StreamingResponse(generate(), media_type="application/json")

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI analysis failed: {str(e)}"
            )

    async def generate_proposal(self, request: ProposalGenerationRequest, tenant_id: int):
        """Generate proposal using AI service."""
        try:
            result = await self.ai_service.generate_proposal(
                request.opportunity_id,
                tenant_id,
                request.template_id,
                request.additional_context
            )

            return result

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Proposal generation failed: {str(e)}"
            )

    async def analyze_opportunity(self, request: AnalyzeOpportunityRequest, tenant_id: int) -> AnalyzeOpportunityResponse:
        """Unified AI analysis endpoint that loads post context server-side."""
        try:
            # Load post from database
            post = self.linkedin_queries.get_post_by_id(request.post_id, tenant_id)
            if not post:
                raise not_found_error("Post", request.post_id)

            # Perform comprehensive AI analysis
            result = await self.ai_service.analyze_opportunity_comprehensive(
                post,
                enable_cache=request.enable_cache
            )

            return AnalyzeOpportunityResponse.model_validate(result)

        except HTTPException:
            # Re-raise HTTP exceptions (like 404 from not_found_error)
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI analysis failed: {str(e)}"
            )

    async def analyze_opportunity_streaming(self, request: AnalyzeOpportunityRequest, tenant_id: int):
        """Streaming version of AI analysis with progressive updates."""
        try:
            # Load post from database
            post = self.linkedin_queries.get_post_by_id(request.post_id, tenant_id)
            if not post:
                raise not_found_error("Post", request.post_id)

            # Create streaming generator
            async def generate():
                async for chunk in self.ai_service.analyze_opportunity_comprehensive_streaming(
                    post,
                    enable_cache=request.enable_cache
                ):
                    yield chunk

            return StreamingResponse(generate(), media_type="application/json")

        except HTTPException:
            # Re-raise HTTP exceptions (like 404 from not_found_error)
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI analysis failed: {str(e)}"
            )