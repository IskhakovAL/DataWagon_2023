from pyflink.datastream import StreamExecutionEnvironment

from pyflink.table import StreamTableEnvironment

import os

from dotenv import load_dotenv

load_dotenv()


env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
EVENTS_TABLE = os.getenv("EVENTS_TABLE")

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_GROUP = os.getenv("KAFKA_GROUP")
KAFKA_TOPIC_NOAGG = os.getenv("KAFKA_TOPIC_NOAGG")
KAFKA_TOPIC_AGG = os.getenv("KAFKA_TOPIC_AGG")


# Настройка источника данных из Kafka
source_ddl = f"""
    CREATE TABLE events (
        carriage_id INT,
        event_date TIMESTAMP(3),
        station_id INT,
        station_dest_id INT,
        train_index STRING,
        WATERMARK FOR event_date AS event_date - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = '{KAFKA_TOPIC_NOAGG}',
        'properties.bootstrap.servers' = '{KAFKA_BROKER}',
        'properties.group.id' = '{KAFKA_GROUP}',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset',
        'json.timestamp-format.standard' = 'ISO-8601'
    )
"""

t_env.execute_sql(source_ddl)

# Выполнение SQL-запроса для агрегации загруженности в 5-минутном окне
result = t_env.sql_query(
    """
    SELECT
        train_index,
        CAST(COLLECT(ROW(carriage_id, station_id, station_dest_id)) AS STRING) AS carriages,
        SESSION_START(event_date, INTERVAL '1' MINUTE) AS session_start,
        SESSION_END(event_date, INTERVAL '1' MINUTE) AS session_end
    FROM events
    GROUP BY train_index, SESSION(event_date, INTERVAL '1' MINUTE);
"""
)

# Настройка слива данных в PostgreSQL
sink_ddl = f"""
            CREATE TABLE postgres_sink (
                `train_index` STRING,
                `carriages` STRING,
                `session_start` TIMESTAMP,
                `session_end` TIMESTAMP
            ) WITH (
              'connector' = 'jdbc',
              'url' = 'jdbc:postgresql://{POSTGRES_HOST}:5435/{POSTGRES_DB}',
              'username' = '{POSTGRES_USER}',
              'password' = '{POSTGRES_PASSWORD}',
              'table-name' = 'Test'
            )
            """

t_env.execute_sql(sink_ddl)

result.execute_insert("postgres_sink")
