import pathlib
import pkgutil
from importlib import import_module

from fastapi import FastAPI

from src.core.config import settings
from src.core.logging_config import get_logger
from src.utils.common_utils import convert_api_path

logger = get_logger(__name__)


def import_routers(app: FastAPI):
    from src.api.api_v1 import __path__ as api_path

    def recursive_import(base_path, package_prefix):
        for _, module_name, is_pkg in pkgutil.iter_modules(base_path):
            full_module_name = f"{package_prefix}.{module_name}"
            try:
                module = import_module(full_module_name)

                if hasattr(module, "router"):
                    app.include_router(
                        module.router, prefix=settings.api_config.api_prefix
                    )

                if is_pkg:
                    sub_path = [str(pathlib.Path(base_path[0]) / module_name)]
                    recursive_import(sub_path, full_module_name)

            except ImportError as e:
                logger.error(f"Import error {full_module_name}: {e}")

    recursive_import(api_path, convert_api_path(settings.api_config.api_path))
