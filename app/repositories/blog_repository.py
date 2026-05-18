from app.schemas.blog_schema import PostCreateSchema
from app.models.blog_models import BlogModel


class BlogRepository:
    """Repository for managing blog posts."""

    async def create_post(self, post_data: PostCreateSchema) -> BlogModel:
        """Create a new blog post."""
        post = BlogModel(**post_data.model_dump())
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
        self, post_id: str, post_data: PostCreateSchema
    ) -> BlogModel | None:
        """Update a blog post by it's ID."""
        post = await BlogModel.get(post_id)

        if not post:
            return None

        post.title = post_data.title
        post.content = post_data.content
        post.category = post_data.category
        post.tags = post_data.tags

        await post.save()
        return post

    async def delete_post(self, post_id: str) -> bool:
        """Delete a blog post by it's ID."""
        post = await BlogModel.get(post_id)

        if not post:
            return False

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
