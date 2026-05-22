from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime


class UserModel(Document):
    """ Model for user data. """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.now)
    