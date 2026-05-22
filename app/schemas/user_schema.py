from pydantic import BaseModel, Field
from datetime import datetime

class UserCreateSchema(BaseModel):
    """ Schema for user data """
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    created_at: datetime

class UserResponseSchema(BaseModel):
    """ Schema for user response data """
    id: str
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