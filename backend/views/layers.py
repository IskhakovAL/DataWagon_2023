from fastapi import APIRouter, WebSocket, Depends
from logging import Logger
import asyncio
import random
import redis.asyncio as redis
from controllers.layer_controller import LayerController
from dependencies.redis_con import get_redis


router = APIRouter(prefix="/api/layers")
layer_controller = LayerController()

logger = Logger(__name__)


@router.websocket("/hexbin")
async def hexbin(websocket: WebSocket, redis_con: redis.Redis = Depends(get_redis)):
    await websocket.accept()
    try:
        while True:
            data = await layer_controller.get_hexbin(redis_con)
            await websocket.send_json(data)
            await asyncio.sleep(random.randint(4, 5))
    except Exception as e:
        logger.error(str(e))


@router.websocket("/federals")
async def federals(websocket: WebSocket, redis_con: redis.Redis = Depends(get_redis)):
    await websocket.accept()
    try:
        while True:
            data = await layer_controller.get_federals(redis_con)
            await websocket.send_json(data)
            await asyncio.sleep(random.randint(2, 3))
    except Exception as e:
        logger.error(str(e))
