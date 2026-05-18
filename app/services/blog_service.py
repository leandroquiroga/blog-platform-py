from fastapi import HTTPException, status
from bson import ObjectId
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import PostCreateSchema, PostResponseSchema
class BlogService:
    def __init__(self, repository: BlogRepository):
        """ Service for managing blog posts. """
        self.repository = repository
        
    async def create_post(self, post_data: PostCreateSchema) -> PostResponseSchema:
        """ Create a new blog post. """
        post = await self.repository.create_post(post_data)
        
        return PostResponseSchema.model_validate(post)
      
    async def get_post(self, post_id: str) -> PostResponseSchema:
        """ Get a blog post by ID. """
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID")
          
        post = await self.repository.get_post(post_id)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
          
        return PostResponseSchema.model_validate(post)
      
      
    async def get_all_posts(self, term: str | None = None) -> list[PostResponseSchema]:
        """ Get all blog posts """
        if term:
            posts = await self.repository.get_posts_by_term(term)
            return [PostResponseSchema.model_validate(post) for post in posts]
        else:
            posts = await self.repository.get_all_posts()
        
        return [PostResponseSchema.model_validate(post) for post in posts]
      
      
    async def update_post(self, post_id: str, post_data: PostCreateSchema) -> PostResponseSchema:
        """ Update a blog post by ID """
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID")
        post = await self.repository.update_post(post_id, post_data)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
          
        return PostResponseSchema.model_validate(post)
      
    async def delete_post(self, post_id: str) -> bool:
        """ Delete a blog post by ID """
        
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID")
        deleted = await self.repository.delete_post(post_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return deleted