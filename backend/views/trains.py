import random

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from aiokafka import AIOKafkaConsumer
import redis.asyncio as redis
import json
import logging
from dependencies.kafka_consumer import get_consumer
from dependencies.redis_con import get_redis
from controllers.train_controller import TrainController

import asyncio

router = APIRouter(prefix="/api/trains")

logger = logging.Logger(__name__)


@router.websocket("/ws")
async def trains_ws(websocket: WebSocket, consumer: AIOKafkaConsumer = Depends(get_consumer)):
    await websocket.accept()
    try:
        while True:
            async for message in consumer:
                await websocket.send_json(
                    TrainController.parse_kafka_message(message.value)
                )
    except WebSocketDisconnect:
        pass


@router.websocket('/amount')
async def trains_amount(websocket: WebSocket):
    await websocket.accept()
    amounts = [10, 77, 189]
    try:
        while True:
            for i in range(len(amounts)):
                await websocket.send_json({'trains_amount': amounts[i]})
                await asyncio.sleep(random.randint(30, 60))
    except Exception as e:
        logger.error(str(e))


@router.websocket('/mult')
async def trains_mult(websocket: WebSocket, redis_con: redis.Redis = Depends(get_redis)):
    await websocket.accept()
    try:
        while True:
            response = await TrainController.get_trains_redis(redis_con)
            await websocket.send_json(response)
            await asyncio.sleep(random.randint(2, 3))
    except Exception as e:
        logger.error(str(e))

