import redis

import config

if config.redis_host is None or config.redis_port is None:
    raise ValueError("redis_host and redis_port must be set")

redis_host = config.redis_host
redis_port = config.redis_port


redis_connection = redis.Redis(
    host=redis_host,
    port=int(redis_port),
)
