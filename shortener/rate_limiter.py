from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

RATE_LIMIT = 20
RATE_LIMIT_EXPIRY = 86400

def check_rate_limit(user_id):
    key = f"rate:user:{user_id}"
    count = cache.get(key)

    #First Request
    if count is None:
        cache.set(key, 1, timeout=RATE_LIMIT_EXPIRY)
        return True
    
    if count >= RATE_LIMIT:
        return False
    
    #Increment Count
    cache.incr(key)
    return True