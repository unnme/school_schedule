from functools import cached_property, lru_cache
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import quote

from pydantic import AnyUrl, BeforeValidator, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.utils.common_utils import parse_cors

from .pathes import base_pathes


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), extra="ignore"
    )


class LoggingConfig(BaseSettings):
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "ERROR"

    _LEVELS = {
        "CRITICAL": 50,
        "FATAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "WARN": 30,
        "INFO": 20,
        "DEBUG": 10,
        "NOTSET": 0,
    }

    @property
    def get_log_level(self) -> int:
        return self._LEVELS[self.LOG_LEVEL]


class BaseConfig(GlobalSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str

    SUPERUSER_MAIL: EmailStr
    SUPERUSER_PASS: str

    ENVIRONMENT: Literal["local", "staging", "production"]

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]


class SecurityConfig(GlobalSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class ApiConfig(GlobalSettings):
    API_VERSION: str

    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"
    service: str = "/service"
    login: str = "/login"
    jwt: str = "/jwt"

    @cached_property
    def api_root_dir_name(self) -> str:
        return base_pathes._api_root_dir.name

    @cached_property
    def api_path(self) -> Path:
        return Path(base_pathes.workdir.name) / "api" / f"api_{self.API_VERSION}"

    @cached_property
    def api_prefix(self) -> str:
        """-> /api/v1"""
        return f"/{self.api_root_dir_name}/{self.API_VERSION}"

    @property
    def bearer_token_url(self) -> str:
        """-> api/v1/auth/login"""
        return f"{self.api_root_dir_name}/{self.API_VERSION}{self.login}"  # BUG: {self.auth}?


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
    logging_config: LoggingConfig


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings(
        base=BaseConfig(),  # pyright: ignore
        security=SecurityConfig(),  # pyright: ignore
        database=DatabaseConfig(),  # pyright: ignore
        api_config=ApiConfig(),  # pyright: ignore
        logging_config=LoggingConfig(),
    )


settings = get_settings()
