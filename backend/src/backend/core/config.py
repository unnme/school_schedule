from functools import cached_property, lru_cache
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import quote

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.pathes import base_pathes
from backend.utils.common_utils import parse_cors


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), env_file_encoding="utf-8", extra="ignore"
    )


class BaseConfig(GlobalSettings):
    BACKEND_APP_NAME: str
    BACKEND_APP_VERSION: str

    ENVIRONMENT: Literal["local", "staging", "production"]


class SecurityConfig(GlobalSettings):
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]


class ApiConfig(GlobalSettings):
    API_VERSION: str
    PAGINATION_LIMIT: int

    @cached_property
    def api_root_dir_name(self) -> str:
        return base_pathes._api_root_dir.name

    @cached_property
    def api_path(self) -> Path:
        return Path(base_pathes.app_root_dir.name) / "api" / f"api_{self.API_VERSION}"

    @cached_property
    def api_prefix(self) -> str:
        """-> /api/v1"""
        return f"/{self.api_root_dir_name}/{self.API_VERSION}"


class DatabaseConfig(GlobalSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def async_db_url(self) -> str:
        password = quote(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class AppSettings(GlobalSettings):
    api_config: ApiConfig
    base: BaseConfig
    security: SecurityConfig
    database: DatabaseConfig


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings(
        base=BaseConfig(),  # pyright: ignore
        security=SecurityConfig(),  # pyright: ignore
        database=DatabaseConfig(),  # pyright: ignore
        api_config=ApiConfig(),  # pyright: ignore
    )


settings = get_settings()
