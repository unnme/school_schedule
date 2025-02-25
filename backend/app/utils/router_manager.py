from importlib import import_module
import pkgutil

from fastapi import FastAPI

from app.core.settings import settings
from app.core.logging_config import logger


def import_routers(app: FastAPI):
    from app.api.api_v1 import __path__ as api_path

    for _, module_name, _ in pkgutil.iter_modules(api_path):
        try:
            module = import_module(f"app.api.api_v1.{module_name}")
            if hasattr(module, "router"):
                app.include_router(module.router, prefix=settings.base.API_V1_STR)
        except ImportError as e:
            logger.error(f"Ошибка импорта {module_name}: {e}")
