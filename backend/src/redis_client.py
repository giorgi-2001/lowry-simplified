from redis import Redis
from datetime import timedelta
import json


redis_client = Redis(
    host="lowry-redis"
)


class RedisClient:
    @staticmethod
    def get_item_from_cachce(key: str):
        item = redis_client.get(name=key)
        if item:
            return json.loads(item)
        return None

    @staticmethod
    def set_item_to_cache(key: str, value, exp: timedelta):
        item_str = json.dumps(value)
        redis_client.setex(name=key, time=exp, value=item_str)

    @staticmethod
    def remove_item(key):
        redis_client.delete(key)
