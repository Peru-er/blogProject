
from django.core.cache import cache
import time

def can_comment(user):
    key = f'comments_{user.id}'
    data = cache.get(key, [])

    now = time.time()
    data = [t for t in data if now - t < 300]

    if len(data) >= 3:
        return False

    data.append(now)
    cache.set(key, data, 300)
    return True
