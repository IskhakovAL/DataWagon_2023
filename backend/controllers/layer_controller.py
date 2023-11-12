import json
import redis.asyncio as redis
import random


class LayerController:
    def __init__(self):
        self.colors = ["#6394D7", "#0C60D4", "#7036BE", "#EB5425"]

    async def _get_color_object(self, obj_name: str, redis_con: redis.Redis):
        redis_data = await redis_con.hget('polygons', obj_name)
        data = json.loads(redis_data)
        for i in range(len(data['features'])):
            data['features'][i]['properties'].update({
                "color": random.choice(self.colors),
                "opacity": 0.3,
                "fillOpacity": 0.09
            })
        return data

    def get_federals(self, redis_con: redis.Redis):
        return self._get_color_object('federals', redis_con)

    def get_hexbin(self, redis_con: redis.Redis):
        return self._get_color_object('hexbin', redis_con)
