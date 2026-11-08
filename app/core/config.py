from enum import StrEnum

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    app_name: str = "Notification Platform"

    app_env: AppEnvironment
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"

    jwt_expiration_minutes: int = 60
    jwt_refresh_expiration_minutes: int = 60 * 24 * 7

    max_file_size: int = 2 * 1024 * 1024

    allowed_content_types: set[str] = {
        "image/jpeg",
        "image/png",
    }

    allowed_extensions: set[str] = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    @model_validator(mode="after")
    def validate_production_settings(self):
        if (
            self.app_env == AppEnvironment.PRODUCTION
            and len(self.jwt_secret) < 32
        ):
            raise ValueError(
                "Production JWT_SECRET must be at least 32 characters"
            )

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
