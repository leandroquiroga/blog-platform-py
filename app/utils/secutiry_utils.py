from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.setting_config import settings


# Hashing context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """ Hashes a password using bcrypt algorithm """
    return pwd_context.hash(password)
  
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies a plain password against a hashed password """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict ) -> str:
    """ Creates a JWT access token with the given data and expiration time """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """ Decodes a JWT access token and returns the payload data """
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None