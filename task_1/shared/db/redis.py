import redis.asyncio as redis
from loguru import logger

from infra.config import config


class Redis:
    redis_client: redis.Redis = None

    @classmethod
    async def connect(cls, host: str = "localhost", port: int = 6379, username=None, password=None):
        try:
            cls.redis_client = redis.Redis(host=host, port=port,
                                           username=username, password=password)
        except redis.RedisError as e:
            logger.error(f"failed to connect redis: {e}")
            raise

        await cls.redis_client

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            await cls.redis_client.aclose()

    @classmethod
    async def insert(cls, key: str, value: str):
        await cls.redis_client.set(key, value)

    @classmethod
    async def get(cls, key: str):
        val = await cls.redis_client.get(key)
        if val is None:
            return None
        val_decoded = val.decode("utf-8")
        return val_decoded


async def run_redis():
    await Redis.connect(host="redis_host", port=6379)
    return Redis
