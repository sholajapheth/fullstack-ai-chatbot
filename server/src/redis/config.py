import os
from dotenv import load_dotenv
import redis

# from rejson import Client

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
            username=self.REDIS_USER,  # use your Redis user. More info https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
            password=self.REDIS_PASSWORD,  # use your Redis password
        )
        return self.connection

    # async def create_rejson_connection(self):
    #     self.redisJson = Client(
    #         host=self.REDIS_HOST,
    #         port=self.REDIS_PORT,
    #         decode_responses=True,
    #         username=self.REDIS_USER,
    #         password=self.REDIS_PASSWORD,
    #     )

    #     return self.redisJson
