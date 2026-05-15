from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings, DatabaseConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Context manager for FastAPI lifespan events."""
    db = DatabaseConfig(settings.URL_MONGO_DB, settings.DATABASE_NAME)
    await db.connect()
    yield
    await db.disconnect()
    
app = FastAPI(
    title = "Blog Project",
    description = "A simple blog project built with FastAPI",
    version = "1.0.0",
    lifespan=lifespan
)


