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

router = APIRouter(prefix="/trains")

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
                # print(type(message.key))
                # await websocket.send_json(message.value)
    except WebSocketDisconnect:
        pass


@router.websocket('/test')
async def train(websocket: WebSocket):
    # a = [55.755793, 56.129014]
    # b = [37.617134, 40.406373]
    stations = [[55.9007, 49.2657],
                [55.9328, 49.3115],
                [55.9423, 49.3301],
                [55.9678, 49.4205],
                [55.9726, 49.4499],
                [55.9942, 49.5078],
                [56.0079, 49.5702],
                [56.0102, 49.6138],
                [56.0226, 49.6476],
                [56.0417, 49.7305],
                [56.0465, 49.7896],
                [56.0566, 49.8224],
                [56.0769, 49.8885]]

    stations2 = [[55.9652, 48.4178],
                 [56.0224, 48.3856],
                 [56.0709, 48.3697],
                 [56.1152, 48.352],
                 [56.1564, 48.3237],
                 [56.2191, 48.2484],
                 [56.31, 48.2502],
                 [56.3811, 48.2032],
                 [56.443, 48.1248],
                 [56.5117, 48.0502],
                 [56.5539, 47.9872],
                 [56.6217, 47.8799],
                 [56.6254, 47.8523]]
    await websocket.accept()
    try:
        while True:
            for station1, station2 in zip(stations, stations2):
                await websocket.send_json([{
                    "train_index": "123",
                    "carriage": [
                        {
                            "carriage_id": ["123", "123"],
                            "station_from_id": ["123", "123"],
                            "station_to_id": ["123", "123"],
                        }
                    ],
                    "current_time": "202020202",
                    "current_station_id": "123",
                    "stations": [
                        {
                            "station_id": "123",
                            "station_time": "2020202",
                            "latitude": row[0],
                            "longitude": row[1]
                        } for row in stations
                    ],
                    "latitude": station1[0],
                    "longitude": station1[1]
                },
                    {
                        "train_index": "456",
                        "carriage": [
                            {
                                "carriage_id": ["123", "123"],
                                "station_from_id": ["123", "123"],
                                "station_to_id": ["123", "123"],
                            }
                        ],
                        "current_time": "202020202",
                        "current_station_id": "123",
                        "stations": [
                            {
                                "station_id": "123",
                                "station_time": "2020202",
                                "latitude": row[0],
                                "longitude": row[1]
                            } for row in stations2
                        ],
                        "latitude": station2[0],
                        "longitude": station2[1]
                    }]
                )
                await asyncio.sleep(random.randint(2, 3))
    except Exception as e:
        logger.error(str(e))


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