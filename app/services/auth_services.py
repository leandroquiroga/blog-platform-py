from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, LoginSchema, TokenSchema
from app.models.user_models import UserModel
from app.utils.secutiry_utils import hash_password, verify_password, create_access_token, decode_access_token

class AuthService:
    """ Authentication service for handling user authentication and authorization """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    async def register_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        """ Register a new user """
        existing_user = await self.user_repository.find_user_by_email(user_data.email)
        
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        hashed_password = hash_password(user_data.password)
        
        user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
        )
        
        await self.user_repository.create_user(user)
        return UserResponseSchema.model_validate(user)
    
    async def login_user(self, login_data: LoginSchema) -> TokenSchema:
        """ Login a user and return an access token """
        user = await self.user_repository.find_user_by_email(login_data.email)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        token = create_access_token({"sub": str(user.id)})
        
        return TokenSchema(access_token=token)
    
    async def get_current_user(self, token: str) -> UserModel:
        """ Get the current authenticated user """
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = await UserModel.get(user_id)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    