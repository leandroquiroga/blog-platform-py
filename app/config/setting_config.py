from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ Configuration settings for the application. """
    URL_MONGO_DB: str = Field(validation_alias="URL_MONGO_DB")
    DATABASE_NAME: str = Field(validation_alias="DATABASE_NAME")
    REDIS_HOST: str = Field(validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(validation_alias="REDIS_DB")
    
    RATE_LIMIT: str = Field(
        default="10/minute",
        validation_alias="RATE_LIMIT",
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings() # pyright: ignore[reportCallIssue]