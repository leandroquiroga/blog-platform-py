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