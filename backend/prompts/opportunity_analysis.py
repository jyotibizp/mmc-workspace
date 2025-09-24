SYSTEM_MESSAGE = "You are an expert at analyzing business opportunities from social media posts. Return only valid JSON."

USER_PROMPT_TEMPLATE = """Analyze this LinkedIn post for business opportunity potential:

POST CONTENT: {post_content}
AUTHOR PROFILE: {author_profile_url}

Provide a comprehensive analysis in JSON format with these fields:

1. is_opportunity: boolean (true if this contains a business opportunity)
2. confidence: float 0-1 (confidence in opportunity detection)
3. extracted_fields: dict with confidence scores for:
   - title: brief opportunity title
   - summary: 1-2 sentence summary
   - problem: what problem needs solving
   - scope: project scope/requirements
   - skills_required: list of skills needed
4. company_suggestion: if company mentioned, null otherwise
   - name: string company name
   - confidence: float 0-1
   - domain: string website domain or null
   - linkedin_url: string company LinkedIn or null
5. contact_suggestion: if contact details found, null otherwise
   - name: string contact person name or null
   - email: string email or null
   - phone: string phone or null
   - linkedin_profile_url: string profile URL or null
   - confidence: float 0-1 (overall confidence)
6. category: classify as 'development', 'consulting', 'design', 'marketing', 'other'
7. urgency: 'urgent', 'normal', 'low'
8. tags: array of relevant skill/domain tags
9. budget_range: if mentioned (e.g. "$5k-10k", "negotiable")
10. timeline: if mentioned (e.g. "2 weeks", "ASAP", "Q1")

Each extracted_field should have: {{"value": "extracted_value", "confidence": 0.85}}

Return only valid JSON."""

MODEL_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 2000
}