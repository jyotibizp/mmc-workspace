from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from services.ai_service import AIService
from schemas.ai import AnalyzeExtractRequest, ProposalGenerationRequest
import json

class AIController:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService(db)

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