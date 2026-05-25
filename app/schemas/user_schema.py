from pydantic import BaseModel, Field
from datetime import datetime
from app.utils.validation_utils import PyObjectId

class UserCreateSchema(BaseModel):
    """ Schema for user data """
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)

class UserResponseSchema(BaseModel):
    """ Schema for user response data """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    username: str
    email: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
class LoginSchema(BaseModel):
    """ Schema for user login data """
    email: str
    password: str
    
class TokenSchema(BaseModel):
    """ Schema for authentication token """
    access_token: str
    token_type: str = "bearer"