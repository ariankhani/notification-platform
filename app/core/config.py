from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Notification Platform"

    database_url: str = "sqlite:///./app.db"

    jwt_secret: str = "CHANGE-ME-SET-IN-ENV-FILE"
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()