import os
from dotenv import load_dotenv
import redis

load_dotenv()


class RedisCn:
    def __init__(self) -> None:
        """init connection"""
        self.REDIS_URL = os.environ["REDIS_URL"]
        self.REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
        self.REDIS_USER = os.environ["REDIS_USER"]
        self.REDIS_HOST = os.environ["REDIS_HOST"]
        self.REDIS_PORT = os.environ["REDIS_PORT"]

    async def create_connection(self):
        self.connection = redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
        )
        return self.connection
