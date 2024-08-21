from src.redis.config import RedisCn
import asyncio


async def main():
    redis = RedisCn()
    redis = await redis.create_connection()
    redis.set("keyst", "values")
    print(redis.get("keys"))
    print(redis)


if __name__ == "__main__":
    asyncio.run(main())
