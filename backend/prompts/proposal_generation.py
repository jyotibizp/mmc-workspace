SYSTEM_MESSAGE = "You are an expert proposal writer for freelancers and agencies."

USER_PROMPT_TEMPLATE = """Generate a professional proposal for the following opportunity:

Title: {title}
Summary: {summary}
Tags: {tags}

Additional context: {additional_context}

Create a comprehensive proposal with the following sections:
1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Timeline and Milestones
5. Investment
6. Why Choose Us
7. Next Steps

Make it professional, concise, and compelling."""

MODEL_CONFIG = {
    "model": "gpt-4-turbo-preview",
    "temperature": 0.7,
    "max_tokens": 2000
}