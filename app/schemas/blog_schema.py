from pydantic import BaseModel, Field
from datetime import datetime


class PostCreateSchema(BaseModel):
    """ Schema for creating a blog post. """
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., min_length=3, max_length=20)
    tags: list[str] = Field(default_factory=list)
    
class PostResponseSchema(PostCreateSchema):
    """ Schema for the response of a blog post. """
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }