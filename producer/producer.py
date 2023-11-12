import psycopg2
from kafka import KafkaProducer
import random
import time
import os
import json

from dotenv import load_dotenv

load_dotenv()

random.seed(time.time())

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

# Параметры подключения к базе данных
db_params = {
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "host": POSTGRES_HOST,
    "port": "5435",
}

connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

producer = KafkaProducer(
    bootstrap_servers=f"{POSTGRES_HOST}:9094",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

row_offset = 0

cursor.execute('SELECT count(*) FROM "trainsmoves"')
total_rows = cursor.fetchone()[0]

while True:
    print("-----")
    if row_offset == total_rows:
        row_offset = 0
    row_limit = random.randint(10, 20)
    print(f"Rows limit: {row_limit}")
    print(f"Rows offset: {row_offset}")
    cursor.execute(
        f'SELECT * FROM "trainsmoves" WHERE id >= {row_offset} LIMIT {row_limit}'
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        cursor.execute(f"SELECT * FROM trainsstations WHERE train_index = '{row[1]}'")
        stations = cursor.fetchone()
        print(stations)
        producer.send(
            "trains",
            key=row[1].encode(),
            value={
                "train_index": row[1],
                "event_date": row[2].isoformat(),
                "carriage_ids": row[3],
                "current_station": row[4],
                "latitude": row[5],
                "longitude": row[6],
                "initial_stations_ids": row[8],
                "final_stations_ids": row[9],
                "station_ids": stations[1],
                "arrival_times": [
                    arrival_time.isoformat() for arrival_time in stations[2]
                ],
                "station_longitudes": [
                    longitude for longitude in stations[3]
                ],
                "station_latitudes": [
                    latitude for latitude in stations[4]
                ]
            },
        )
    row_offset = rows[-1][0] + 1
