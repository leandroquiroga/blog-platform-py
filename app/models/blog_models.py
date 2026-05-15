from pydantic import Field
from beanie import  Document
from datetime import datetime

class BlogModel(Document):
    """ Model for a blog post. """
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., min_length=3, max_length=20)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now) 
    