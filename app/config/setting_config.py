from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the application."""

    URL_MONGO_DB: str = Field(validation_alias="URL_MONGO_DB")
    DATABASE_NAME: str = Field(validation_alias="DATABASE_NAME")
    REDIS_HOST: str = Field(validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(validation_alias="REDIS_DB")
    JWT_SECRET_KEY: str = Field(validation_alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(validation_alias="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    RATE_LIMIT: str = Field(
        default="10/minute",
        validation_alias="RATE_LIMIT",
    )

    @property
    def rate_limit_count(self) -> int:
        """Extract the count from the RATE_LIMIT string."""
        return int(self.RATE_LIMIT.split("/")[0])

    @property
    def rate_limit_window(self) -> int:
        """Extract the time window in seconds from the RATE_LIMIT string."""
        period = self.RATE_LIMIT.split("/")[1]
        return {"minute": 60, "hour": 3600, "day": 86400}[period]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()  # pyright: ignore[reportCallIssue]
