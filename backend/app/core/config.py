import os
from pathlib import Path
from urllib.parse import quote
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.common_utils import parse_cors


def is_running_in_docker() -> bool:
    return (
        os.path.exists("/.dockerenv") or "docker" in Path("/proc/1/cgroup").read_text()
    )


if not is_running_in_docker():
    _PROJECT_ROOT_DIR: Path = Path.cwd().parents[2]
    _ENV_FILE = _PROJECT_ROOT_DIR / ".env"
else:
    _PROJECT_ROOT_DIR = Path("/app")
    _ENV_FILE = None


class LoggingConfig(BaseSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class ApiPrefix(BaseSettings):
    API_PREFIX: str = "/api"
    API_VERSION_PERFIX: str = "v1"

    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"
    service: str = "/service"
    login: str = "/login"
    jwt: str = "/jwt"

    def __init__(self, **data):
        super().__init__(**data)
        if not self.API_VERSION_PERFIX.startswith("/"):
            self.API_VERSION_PERFIX = f"/{self.API_VERSION_PERFIX}"

    @property
    def get_api_prefix(self) -> str:
        """-> /api/v1"""
        return f"{self.API_PREFIX}{self.API_VERSION_PERFIX}"

    @property
    def bearer_token_url(self) -> str:
        """-> api/v1/auth/login"""
        return f"{self.API_PREFIX}{self.API_VERSION_PERFIX}{self.login}"


class BaseConfig(BaseSettings):
    BACKEND_APPS_DIR: Path = _PROJECT_ROOT_DIR / "app"
    API_V1_DIR: Path = BACKEND_APPS_DIR / "api" / "api_v1"
    ENTITIES_DIR: Path = BACKEND_APPS_DIR / "entities"

    ENVIRONMENT: Literal["local", "staging", "production"]
    PROJECT_NAME: str
    PROJECT_VERSION: str
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


class SecurityConfig(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


class DatabaseConfig(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def sync_db_url(self) -> str:
        password = quote(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_db_url(self) -> str:
        password = quote(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


class AppSettings(BaseSettings):
    api_prefix: ApiPrefix
    base: BaseConfig
    security: SecurityConfig
    database: DatabaseConfig
    logging_config: LoggingConfig

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings(
        base=BaseConfig(), # pyright: ignore
        security=SecurityConfig(), # pyright: ignore
        database=DatabaseConfig(), # pyright: ignore
        api_prefix=ApiPrefix(),
        logging_config=LoggingConfig(),
    )


settings = get_settings()
