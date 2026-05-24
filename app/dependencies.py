def get_blog_service():
    """ Dependency to get the BlogService instance. """
    from app.services.blog_service import BlogService
    from app.repositories.blog_repository import BlogRepository
    repository = BlogRepository()
    cache = get_cache_utils()
    service = BlogService(repository, cache)
    return service
  


def get_cache_utils():
    """ Dependency to get the CacheUtils instance. """
    from app.config.redis_config import redis_client
    from app.utils.cache_utils import CacheUtils
    
    return CacheUtils(redis_client)

from app.services.auth_services import AuthService
from app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,  HTTPAuthorizationCredentials
from app.models.user_models import UserModel

security = HTTPBearer(auto_error=False)


# Dependency to get the AuthService instance
def get_auth_service():
    """ Dependency to get the AuthService instance. """
    
    repository =  UserRepository()
    service = AuthService(repository)
    return service



async def get_current_user(   
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service),) -> UserModel:
    """ Dependency to get the current authenticated user """
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return await service.get_current_user(credentials.credentials)
    