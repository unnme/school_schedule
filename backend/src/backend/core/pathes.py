from functools import cached_property
from pathlib import Path


class BasePathes:
    def __init__(self):
        self._project_root_dir = Path("/app")
        self._env_file = self._project_root_dir / ".env.docker"
        self._app_root_dir = self._project_root_dir / "src" / "backend"
        self._entities_dir = self._app_root_dir / "entities"
        self._api_root_dir = self._app_root_dir / "api"
        self._workdir = self._project_root_dir / "src"
        self._logs_path = self._workdir / "logs"

    @cached_property
    def logs_path(self) -> Path:
        return self._logs_path

    @cached_property
    def app_root_dir(self) -> Path:
        return self._app_root_dir

    @cached_property
    def workdir(self) -> Path:
        return self._project_root_dir

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
