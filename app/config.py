from typing import Any

from envparse import env
from pydantic import Field, validator
from pydantic_settings import BaseSettings

env.read_envfile()


POSTGRES_HOST = env("POSTGRES_HOST", cast=str)
POSTGRES_PORT = env("POSTGRES_PORT", cast=int)
POSTGRES_USER = env("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", cast=str)
POSTGRES_DB = env("POSTGRES_DB", cast=str)
API_CLIENT_KEY = env("API_CLIENT_KEY", cast=str)

POSTGRES_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)


class Config(BaseSettings):
    APP_TITLE: str = Field("curreny_exchanger")
    DEBUG: bool = True

    POSTGRES_HOST: str = Field(...)
    POSTGRES_PORT: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    DATABASE_URL: str | None = None

    @validator("DATABASE_URL", pre=True)
    def build_database_url(
        cls, value: str | None, values: dict[str, Any], **kwargs
    ) -> str:
        if isinstance(value, str):
            return value
        url = POSTGRES_URL
        return url


settings = Config(_env_file=".env", _env_file_encoding="utf-8")
