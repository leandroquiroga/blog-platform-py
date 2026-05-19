from app.services.blog_service import BlogService
from app.repositories.blog_repository import BlogRepository
from app.utils.cache_utils import CacheUtils
from app.config.redis_config import RedisConfig

def get_blog_service() -> BlogService:
    """ Dependency to get the BlogService instance. """
    repository = BlogRepository()
    service = BlogService(repository)
    return service
  
def get_cache_utils() -> CacheUtils:
    """ Dependency to get the CacheUtils instance. """
    redis_config = RedisConfig()
    cache = CacheUtils(redis_config)
    return cache