from fastapi import HTTPException, status
from bson import ObjectId
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import PostCreateSchema, PostResponseSchema
from app.utils.cache_utils import CacheUtils


class BlogService:
    def __init__(self, repository: BlogRepository, cache: CacheUtils | None = None):
        """Service for managing blog posts."""
        self.repository = repository
        self.cache = cache

    async def create_post(self, post_data: PostCreateSchema, author_id: str) -> PostResponseSchema:
        """Create a new blog post."""
        post = await self.repository.create_post(post_data, author_id)

        #Invalid cache after creating a new post
        if self.cache:
            await self.cache.clear_cache("posts:all")
            await self.cache.clear_cache(f"posts:search:*")
            await self.cache.clear_cache(f"posts:author:{author_id}")
            
        return PostResponseSchema.model_validate(post)

    async def get_post(self, post_id: str) -> PostResponseSchema:
        """Get a blog post by ID."""

        if not ObjectId.is_valid(post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID"
            )

        if self.cache:
            cache_key = f"post:{post_id}"
            cache_data = await self.cache.get_cache(cache_key)

            if cache_data:
                return PostResponseSchema(**cache_data)

        post = await self.repository.get_post(post_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        if self.cache:
            await self.cache.set_cache(cache_key, post.model_dump(mode="json"), expire=600)
        return PostResponseSchema.model_validate(post)

    async def get_all_posts(self, term: str | None = None) -> list[PostResponseSchema]:
        """Get all blog posts"""
        if term:
            if self.cache:
                cache_key = f"posts:search:{term}"
                cache_data = await self.cache.get_cache(cache_key)
                if cache_data:
                    return [PostResponseSchema(**post) for post in cache_data]
            
            posts = await self.repository.get_posts_by_term(term)

            if self.cache:
                await self.cache.set_cache(cache_key, [post.model_dump(mode="json") for post in posts], expire=600)
            return [PostResponseSchema.model_validate(post) for post in posts]
        else:
            if self.cache:
                cache_key = "posts:all"
                cache_data = await self.cache.get_cache(cache_key)
                if cache_data:
                    return [PostResponseSchema(**post) for post in cache_data]
            
            posts = await self.repository.get_all_posts()
            if self.cache:
                await self.cache.set_cache(cache_key, [post.model_dump(mode="json") for post in posts], expire=600)

        return [PostResponseSchema.model_validate(post) for post in posts]

    async def update_post(
        self, post_id: str, post_data: PostCreateSchema, author_id: str
    ) -> PostResponseSchema:
        """Update a blog post by ID"""

        if not ObjectId.is_valid(post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID"
            )
        post = await self.repository.update_post(post_id, post_data, author_id)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        if self.cache:
            await self.cache.clear_cache(f"post:{post_id}")
            await self.cache.clear_cache("posts:all")
            await self.cache.clear_cache(f"posts:search:*")
            await self.cache.clear_cache(f"posts:author:{author_id}")
            
        return PostResponseSchema.model_validate(post)

    async def delete_post(self, post_id: str, author_id: str) -> bool:
        """Delete a blog post by ID"""

        if not ObjectId.is_valid(post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID"
            )
        deleted = await self.repository.delete_post(post_id, author_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        if self.cache:
            await self.cache.clear_cache(f"post:{post_id}")
            await self.cache.clear_cache("posts:all")
            await self.cache.clear_cache(f"posts:search:*")
            await self.cache.clear_cache(f"posts:author:{author_id}")

        return deleted

    async def get_my_posts(self, author_id: str) -> list[PostResponseSchema]:
        """ Get all blog posts created by the authenticated user """
        if self.cache:
            cache_key = f"posts:author:{author_id}"
            cache_data = await self.cache.get_cache(cache_key)
            if cache_data:
                return [PostResponseSchema(**post) for post in cache_data]
            
        posts = await self.repository.get_post_by_id(author_id)
        if self.cache:
            await self.cache.set_cache(cache_key, [post.model_dump(mode="json") for post in posts], expire=600)
        return [PostResponseSchema.model_validate(post) for post in posts]