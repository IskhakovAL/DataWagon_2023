import json

import redis.asyncio as redis


class TrainController:

    @staticmethod
    def parse_kafka_message(message: dict):
        return {
            "train_index": message['train_index'],
            "carriage": [
                {
                    "carriage_id": message['carriage_ids'][i],
                    "station_from_id": message['initial_stations_ids'][i],
                    "station_to_id": message['final_stations_ids'][i],
                } for i in range(len(message['carriage_ids']))
            ],
            "current_time": message['event_date'],
            "current_station_id": message['current_station'],
            "stations": [
                {
                    "station_id": message['station_ids'][i],
                    "station_time": message['arrival_times'][i],
                    "latitude": message['station_latitudes'][i],
                    "longitude": message['station_longitudes'][i]
                } for i in range(len(message['station_ids']))
            ],
            "latitude": message['latitude'],
            "longitude": message['longitude']
        }

    @staticmethod
    async def get_trains_redis(redis_con: redis.Redis):
        trains_events = await redis_con.hgetall('trains')
        resp = []
        for train_event_json in trains_events.values():
            train_event = json.loads(train_event_json)
            resp.append({
                "train_index": train_event['train_index'],
                "carriage": [
                    {
                        "carriage_id": train_event['carriage_ids'][i],
                        "station_from_id": train_event['initial_stations_ids'][i],
                        "station_to_id": train_event['final_stations_ids'][i],
                    } for i in range(len(train_event['carriage_ids']))
                ],
                "current_time": train_event['event_date'],
                "current_station_id": train_event['current_station'],
                "stations": [
                    {
                        "station_id": train_event['station_ids'][i],
                        "station_time": train_event['arrival_times'][i],
                        "latitude": train_event['station_latitudes'][i],
                        "longitude": train_event['station_longitudes'][i]
                    } for i in range(len(train_event['station_ids']))
                ],
                "latitude": train_event['latitude'],
                "longitude": train_event['longitude']
            })
        return resp
