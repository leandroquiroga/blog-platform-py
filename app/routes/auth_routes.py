from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_services import AuthService
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, LoginSchema, TokenSchema
from app.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security dependency for protected routes
security = HTTPBearer(auto_error=False)

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema, service: AuthService = Depends(get_auth_service)):
    return await service.register_user(user_data)

@router.post("/login", response_model=TokenSchema)
async def login_user(login_data: LoginSchema, service: AuthService = Depends(get_auth_service)):
    return await service.login_user(login_data)

@router.get("/me", response_model=UserResponseSchema)
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security), service: AuthService = Depends(get_auth_service)):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return await service.get_current_user(credentials.credentials)
    