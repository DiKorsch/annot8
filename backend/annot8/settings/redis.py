import logging
import os

redis_url = os.environ.get('REDIS_HOST', '127.0.0.1')

logging.info(f"Using redis server: {redis_url}")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{redis_url}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
