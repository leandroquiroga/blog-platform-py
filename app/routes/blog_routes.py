from fastapi import APIRouter, status, Depends
from app.services.blog_service import BlogService
from app.schemas.blog_schema import PostCreateSchema, PostResponseSchema
from app.dependencies import get_blog_service

router = APIRouter(prefix="/api/v1/posts", tags=["Blog"])

@router.get("/", response_model=list[PostResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_posts(term: str | None = None, service: BlogService = Depends(get_blog_service)):
    return await service.get_all_posts(term)
 
@router.get("/{post_id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def get_post(post_id: str, service: BlogService = Depends(get_blog_service)):
    return await service.get_post(post_id)
  
@router.post("/", response_model=PostResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreateSchema, service: BlogService = Depends(get_blog_service)):
    return await service.create_post(post_data)
  
@router.put("/{post_id}", response_model=PostResponseSchema, status_code=status.HTTP_200_OK)
async def update_post(post_id: str, post_data: PostCreateSchema, service: BlogService = Depends(get_blog_service)):
    return await service.update_post(post_id, post_data)
  
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, service: BlogService = Depends(get_blog_service)):
    await service.delete_post(post_id)