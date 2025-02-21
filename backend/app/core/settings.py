from functools import lru_cache
import os
from pathlib import Path
from typing import Literal
from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


def is_running_in_docker() -> bool:
    return os.path.exists("/.dockerenv") or "docker" in Path("/proc/1/cgroup").read_text()

if not is_running_in_docker():
    _PROJECT_ROOT_DIR: Path = Path.cwd().parents[2]
    _ENV_FILE = _PROJECT_ROOT_DIR / ".env"
else:
    _PROJECT_ROOT_DIR = Path("/app")
    _ENV_FILE = None


class BaseConfig(BaseSettings):

    BACKEND_APPS_DIR: Path = _PROJECT_ROOT_DIR / "app"
    API_V1_DIR: Path = BACKEND_APPS_DIR / "api" / "api_v1"
    ENTITIES_DIR: Path = BACKEND_APPS_DIR / "entities"

    ENVIRONMENT: Literal["local", "staging", "production"]
    API_V1_STR: str
    PROJECT_NAME: str
    PROJECT_VERSION: str

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


# ======= Настройки безопасности =======
class SecurityConfig(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


# ======= Настройки базы данных =======
class DatabaseConfig(BaseSettings):

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DB_ECHO: bool

    @property
    def sync_db_url(self) -> str:
        password = quote(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_db_url(self) -> str:
        password = quote(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


# ======= Глобальные настройки =======
class AppSettings(BaseSettings):
    base: BaseConfig
    security: SecurityConfig
    database: DatabaseConfig

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


@lru_cache()
def get_settings():
    return AppSettings(
        base=BaseConfig(), # pyright: ignore
        security=SecurityConfig(), # pyright: ignore
        database=DatabaseConfig(), # pyright: ignore
    )


settings = get_settings()
