from functools import cached_property
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import quote

from pydantic import AnyUrl, BeforeValidator, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.common_utils import is_running_in_docker, parse_cors


class BasePathes:
    def __init__(self):
        if is_running_in_docker():
            self._project_root_dir = Path("/app")
            self._env_file = self._project_root_dir / ".env.docker"
        else:
            self._project_root_dir: Path = Path.cwd().parents[2]
            self._env_file = self._project_root_dir / ".env"

        self._app_root_dir = self._project_root_dir / "src"
        self._entities_dir = self._app_root_dir / "entities"
        self._api_root_dir = self._app_root_dir / "api"

    @cached_property
    def workdir(self) -> Path:
        return self._app_root_dir

    @cached_property
    def env_file(self) -> Path:
        return self._env_file

    @cached_property
    def entities_dir(self) -> Path:
        return self._entities_dir

    @cached_property
    def api_root_dir(self) -> Path:
        return self._api_root_dir


base_pathes = BasePathes()


class Pathes(BasePathes):
    pass


class LoggingConfig(BaseSettings):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class BaseConfig(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str

    SUPERUSER_MAIL: EmailStr
    SUPERUSER_PASS: str

    ENVIRONMENT: Literal["local", "staging", "production"]

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]

    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), extra="ignore"
    )


class SecurityConfig(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), extra="ignore"
    )


class ApiConfig(BaseSettings):
    API_VERSION: str

    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"
    service: str = "/service"
    login: str = "/login"
    jwt: str = "/jwt"

    @property
    def api_root_dir_name(self) -> str:
        return base_pathes._api_root_dir.name

    @property
    def api_path(self) -> Path:
        return Path(base_pathes.workdir.name) / "api" / f"api_{self.API_VERSION}"

    @property
    def api_prefix(self) -> str:
        """-> /api/v1"""
        return f"/{self.api_root_dir_name}/{self.API_VERSION}"

    @property
    def bearer_token_url(self) -> str:
        """-> api/v1/auth/login"""
        return f"{self.api_root_dir_name}/{self.API_VERSION}{self.login}"  # BUG: {self.auth}?

    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), extra="ignore"
    )


class DatabaseConfig(BaseSettings):
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

    model_config = SettingsConfigDict(
        env_file=str(base_pathes.env_file), extra="ignore"
    )


class AppSettings(BaseSettings):
    pathes: Pathes
    api_config: ApiConfig
    base: BaseConfig
    security: SecurityConfig
    database: DatabaseConfig
    logging_config: LoggingConfig


def get_settings() -> AppSettings:
    return AppSettings(
        pathes=Pathes(),  # pyright: ignore
        base=BaseConfig(),  # pyright: ignore
        security=SecurityConfig(),  # pyright: ignore
        database=DatabaseConfig(),  # pyright: ignore
        api_config=ApiConfig(),  # pyright: ignore
        logging_config=LoggingConfig(),
    )


settings = get_settings()


if __name__ == "__main__":
    print(settings.api_config.api_path)
    print(settings.api_config.api_prefix)
    print(settings.api_config.bearer_token_url)
