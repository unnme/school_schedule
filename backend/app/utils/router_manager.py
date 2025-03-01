from importlib import import_module
import logging
import pkgutil
import pathlib

from fastapi import FastAPI

from app.core.config import settings

logger = logging.getLogger(__name__)


def import_routers(app: FastAPI): 
    from app.api.api_v1 import __path__ as api_path

    def recursive_import(base_path, package_prefix):
        for _, module_name, is_pkg in pkgutil.iter_modules(base_path):
            full_module_name = f"{package_prefix}.{module_name}"
            try:
                module = import_module(full_module_name)

                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=settings.api_prefix.v1_prefix)

                if is_pkg:
                    sub_path = [str(pathlib.Path(base_path[0]) / module_name)]
                    recursive_import(sub_path, full_module_name)

            except ImportError as e:
                logger.error(f"Ошибка импорта {full_module_name}: {e}")

    recursive_import(api_path, "app.api.api_v1")
