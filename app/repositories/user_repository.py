from app.models.user_models import UserModel

class UserRepository:
    """ Repository for the UserModel. """
    async def create_user(self, user: UserModel) -> UserModel:
        """ Create a new user """
        await user.save()
        return user
    
    async def find_user_by_email(self, email: str) -> UserModel | None:
        """ Find a user by email """
        
        return await UserModel.find_one(UserModel.email == email)