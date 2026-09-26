from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PATHWISE_")

    environment: Literal["local", "test", "production"] = "local"
    app_name: str = "Pathwise API"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
