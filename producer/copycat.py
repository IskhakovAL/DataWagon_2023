from kafka import KafkaConsumer
from redis import Redis

import os
import json
import random
import time
from string import digits, ascii_letters

from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv('POSTGRES_HOST')

random.seed(time.time())

consumer = KafkaConsumer(
        "trains",
        bootstrap_servers=f"{SERVER}:9094",
        # auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=''.join([random.choice(ascii_letters + digits) for _ in range(random.randint(7, 10))]),
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

redis_con = Redis(host=SERVER, port=6379, decode_responses=True)

while True:
    for message in consumer:
        value = message.value
        print(value)
        redis_con.hset('trains', value['train_index'], json.dumps(value))

