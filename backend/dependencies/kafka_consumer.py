import os

from aiokafka import AIOKafkaConsumer
import json
import random
import time
from string import digits, ascii_letters

from dotenv import load_dotenv
load_dotenv()

KAFKA_SERVER = os.getenv('POSTGRES_HOST')

random.seed(time.time())


async def get_consumer():
    consumer = AIOKafkaConsumer(
        "trains",
        bootstrap_servers=f"{KAFKA_SERVER}:9094",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=''.join([random.choice(ascii_letters+digits) for _ in range(random.randint(7, 10))]),
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()
