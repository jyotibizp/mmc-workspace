SYSTEM_MESSAGE = "You are an expert at analyzing business opportunities from social media posts."

USER_PROMPT_TEMPLATE = """Analyze the following LinkedIn post and extract:
1. Is there a business opportunity?
2. Company information (name, domain, etc.)
3. Contact information (name, role, etc.)
4. Opportunity details (what they need, budget, timeline)
5. Urgency level (High/Medium/Low)
6. Classification/categories

Post content:
{post_content}

Author profile: {author_profile_url}

Return as JSON with the following structure:
{{
    "opportunity_detected": boolean,
    "company_info": {{"name": string, "domain": string}},
    "contact_info": {{"name": string, "role": string}},
    "opportunity_details": {{"title": string, "summary": string, "requirements": []}},
    "urgency": string,
    "classification": [string],
    "confidence_score": float
}}"""

MODEL_CONFIG = {
    "model": "gpt-4-turbo-preview",
    "response_format": {"type": "json_object"},
    "temperature": 0.3
}