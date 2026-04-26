import random
import string
from urllib.parse import urlparse
from .models import Shorturl

def extract_domain_prefix(url, max_chars=8):
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.replace('www.', '')
        domain = netloc.split('.')[0]
        domain = ''.join(c for c in domain if c.isalnum())
        return domain[:max_chars]
    except Exception:
        return ''

def generate_slug(url, random_length=4):
    char = string.ascii_letters + string.digits
    domain_prefix = extract_domain_prefix(url)

    while True:
        random_part = ''.join(random.choices(char, k=random_length))
        if domain_prefix:
            slug = f"{domain_prefix}-{random_part}"
        else:
            slug = ''.join(random.choices(char,k=6))
        
        if not Shorturl.objects.filter(slug=slug).exists():
            return slug