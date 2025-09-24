from typing import Optional
import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_linkedin_url(url: str) -> bool:
    """Validate if a URL is a LinkedIn URL."""
    if not validate_url(url):
        return False

    parsed = urlparse(url)
    return parsed.netloc.lower() in ['linkedin.com', 'www.linkedin.com']

def validate_email(email: str) -> bool:
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def normalize_domain(domain: Optional[str]) -> Optional[str]:
    """Normalize domain by removing protocol and www."""
    if not domain:
        return None

    domain = domain.lower().strip()

    # Remove protocol
    if domain.startswith(('http://', 'https://')):
        domain = domain.split('://', 1)[1]

    # Remove www.
    if domain.startswith('www.'):
        domain = domain[4:]

    # Remove trailing slash
    domain = domain.rstrip('/')

    return domain