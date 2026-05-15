from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.models.blog_models import BlogModel


class DatabaseConfig:
    """ Database configuration for MongoDB. """
    def __init__(self, url: str, database_name: str):
        self.url = url
        self.database_name = database_name
        self.client: AsyncMongoClient | None = None
        
        
    async def connect(self):
        """ Connect to the MongoDB database """
        self.client = AsyncMongoClient(self.url)
        database = self.client[self.database_name]
        
        await init_beanie(database, document_models=[BlogModel])
        
        return database
      
    async def disconnect(self):
        """ Disconnect from the MongoDB database """
        if self.client:
            await self.client.close()