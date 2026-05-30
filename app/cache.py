import json

import redis.asyncio as redis

from app.core.config import REDIS_URL


def create_redis_client():
    return redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )


async def close_redis_client(client):
    try:
        await client.aclose()
    except Exception:
        pass


async def get_cache(key: str):
    client = create_redis_client()

    try:
        data = await client.get(key)

        if data is None:
            return None

        return json.loads(data)
    except Exception:
        return None
    finally:
        await close_redis_client(client)


async def set_cache(key: str, value, seconds: int = 60):
    client = create_redis_client()

    try:
        data = json.dumps(value, ensure_ascii=False)
        await client.set(key, data, ex=seconds)
    except Exception:
        return None
    finally:
        await close_redis_client(client)


async def delete_cache(key: str):
    client = create_redis_client()

    try:
        await client.delete(key)
    except Exception:
        return None
    finally:
        await close_redis_client(client)


async def clear_cache():
    client = create_redis_client()

    try:
        await client.flushdb()
    except Exception:
        return None
    finally:
        await close_redis_client(client)