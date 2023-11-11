import redis.asyncio as redis

import os
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv('POSTGRES_HOST')


async def get_redis():
    client = redis.Redis(host=SERVER, port=6379, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()
