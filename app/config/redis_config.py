from redis.asyncio import Redis
from app.config import settings

redis_client: Redis | None = None

async def connect_redis():
    """ Connect to Redis """
    global redis_client
    
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    
    await redis_client.ping()  # pyright: ignore[reportGeneralTypeIssues]
    
async def disconnect_redis():
    """ Disconnect from Redis """
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None