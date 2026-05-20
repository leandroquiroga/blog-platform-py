from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.blog_routes import router as blog_router
from app.config.database_config import DatabaseConfig
from app.config.redis_config import connect_redis, disconnect_redis
from app.config.setting_config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Context manager for FastAPI lifespan events."""
    db = DatabaseConfig(settings.URL_MONGO_DB, settings.DATABASE_NAME)
    await db.connect()
    await connect_redis()
    yield
    await db.disconnect()
    await disconnect_redis()
    
app = FastAPI(
    title = "Blog Project",
    description = "A simple blog project built with FastAPI",
    version = "1.0.0",
    lifespan=lifespan
)


# Routes
app.include_router(blog_router)
