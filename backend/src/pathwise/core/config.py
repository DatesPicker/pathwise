from functools import lru_cache
from typing import Literal
from urllib.parse import urlsplit

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PATHWISE_",
        env_file=".env.local",
        env_file_encoding="utf-8",
    )

    environment: Literal["local", "test", "production"] = "local"
    app_name: str = "Pathwise API"
    cors_allowed_origin: str

    @field_validator("cors_allowed_origin")
    @classmethod
    def validate_cors_allowed_origin(cls, value: str) -> str:
        origin = urlsplit(value)
        if (
            origin.scheme not in {"http", "https"}
            or not origin.netloc
            or origin.path
            or origin.query
            or origin.fragment
        ):
            raise ValueError("must be an HTTP(S) origin without a path")
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
