import time
import uuid
import redis
import logging

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def is_rate_limited(client_ip: str, limit: int, window_seconds: int) -> bool:
    try:
        key = f"ratelimit:{client_ip}"
        now = time.time()
        member = f"{now} - {uuid.uuid4()}"

        redis_client.zremrangebyscore(key, 0, now - window_seconds)
        redis_client.zadd(key, {member: now})
        count = redis_client.zcard(key)

        return count > limit
    except redis.exceptions.RedisError as e:
        # Fail open: if Redis is down, allow the request rather than
        # break the whole feature. Means rate limiting is off until Redis recovers.
        logging.warning("redis got disconnected %s", e)
        return False
