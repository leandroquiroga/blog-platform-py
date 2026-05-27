from fastapi import HTTPException, status
from app.schemas.blog_schema import PostCreateSchema
from app.models.blog_models import BlogModel
from datetime import datetime

class BlogRepository:
    """Repository for managing blog posts."""

    async def create_post(self, post_data: PostCreateSchema, author_id: str) -> BlogModel:
        """Create a new blog post."""
        post = BlogModel(**post_data.model_dump(), author_id=author_id)
        await post.insert()
        return post

    async def get_post(self, post_id: str) -> BlogModel | None:
        """Get a blog post by it's ID."""
        post = await BlogModel.get(post_id)

        if not post:
            return None

        return post

    async def get_all_posts(self) -> list[BlogModel]:
        """Get all blog posts."""
        return await BlogModel.find_all().to_list()

    async def update_post(
        self, post_id: str, post_data: PostCreateSchema, author_id: str
    ) -> BlogModel | None:
        """Update a blog post by it's ID."""
        post = await BlogModel.get(post_id)

        if not post:
            return None
        
        if post.author_id != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post"
            )

        post.title = post_data.title
        post.content = post_data.content
        post.category = post_data.category
        post.tags = post_data.tags
        post.author_id = author_id
        post.updated_at = datetime.now()
        await post.save()
        return post

    async def delete_post(self, post_id: str, author_id: str) -> bool:
        """Delete a blog post by it's ID."""
        post = await BlogModel.get(post_id)

        if not post:
            return False

        if post.author_id != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post"
            )

        await post.delete()
        return True

    async def get_posts_by_term(self, search_term: str) -> list[BlogModel]:
        """Get blog posts by search term"""
        import re

        regex = re.compile(f".*{re.escape(search_term)}.*", re.IGNORECASE)

        posts = await BlogModel.find(
            (BlogModel.title == regex)
            | (BlogModel.content == regex)
            | (BlogModel.category == regex)
        ).to_list()
        return posts

    async def get_post_by_id(self, user_id: str) -> list[BlogModel]:
        """ Get blog post by user ID """
        return await BlogModel.find(BlogModel.author_id == user_id).to_list()