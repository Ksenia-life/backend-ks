import json

import redis.asyncio as redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)


async def get_cache(key: str):
    data = await redis_client.get(key)

    if data is None:
        return None

    return json.loads(data)


async def set_cache(key: str, value, seconds: int = 60):
    data = json.dumps(value, ensure_ascii=False)
    await redis_client.set(key, data, ex=seconds)


async def delete_cache(key: str):
    await redis_client.delete(key)
    
async def clear_cache():
    await redis_client.flushdb()