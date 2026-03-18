import redis
from app.config.settings import settings

class RedisService:
    def __init__(self):
        self._client: redis.Redis | None = None

    def connect(self) -> None:
        """Create the Redis connection pool."""
        self._client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
        )

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self.connect()
        return self._client

    # counter

    def increment_counter(self) -> int:
        return self.client.incr(settings.REDIS_COUNTER_KEY)

    def get_counter(self) -> int:
        """Return the current value of the global visit counter."""
        value = self.client.get(settings.REDIS_COUNTER_KEY)
        return int(value) if value else 0

    # introspection

    def get_all_keys(self) -> dict:
        """Return all keys and their values (for the /redis-data route)."""
        data: dict = {}
        for key in self.client.keys("*"):
            key_type = self.client.type(key)
            if key_type == "string":
                data[key] = self.client.get(key)
            elif key_type == "list":
                data[key] = self.client.lrange(key, 0, -1)
            elif key_type == "set":
                data[key] = list(self.client.smembers(key))
            elif key_type == "hash":
                data[key] = self.client.hgetall(key)
            elif key_type == "zset":
                data[key] = self.client.zrange(key, 0, -1, withscores=True)
            else:
                data[key] = f"<{key_type}>"
        return data

    # health

    def ping(self) -> bool:
        """Return True if Redis is reachable."""
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False


# Singleton instance shared across the app
redis_service = RedisService()
