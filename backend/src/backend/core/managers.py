import asyncio
import pathlib
import pkgutil
from importlib import import_module

from fastapi import FastAPI
from sqlalchemy import inspect, text

from backend.core.config import settings
from backend.core.pathes import base_pathes
from backend.core.database import session_manager
from backend.core.logging_config import get_logger
from backend.entities.base import Base
from backend.utils.common_utils import path_to_dotted_string


logger = get_logger(__name__)

class ImportManager:

    @classmethod
    def _import_routers(cls, app: FastAPI):
        from backend.api.api_v1 import __path__ as api_path

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

                except ImportError as e:  # FIX:
                    logger.error(f"Import error {full_module_name}: {e}")

        recursive_import(api_path, path_to_dotted_string(settings.api_config.api_path))


    @classmethod
    def _import_entity_models(cls):
        for app_dir in base_pathes.entities_dir.iterdir():
            if app_dir.is_dir() and not app_dir.name.startswith("_"):
                models_file = app_dir / "models.py"
                if models_file.exists():
                    module_name = f"backend.entities.{app_dir.name}.models"
                    import_module(module_name)

    @classmethod
    def base_init(cls, app):
        cls._import_routers(app)
        cls._import_entity_models()



class DatabaseManager:
    @staticmethod
    async def drop_all_tables() -> None:
        try:
            async with session_manager.async_engine.begin() as conn:
                await conn.execute(text("DROP SCHEMA public CASCADE"))
                await conn.execute(text("CREATE SCHEMA public"))
                await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
                await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
            logger.warning("⚠️  Tables have been dropped")
        except Exception as e:
            logger.error(f"Error during drop_all_tables: {e}")

    @staticmethod
    async def create_db_tables() -> None:
        if settings.base.ENVIRONMENT == "local":
            try:
                async with session_manager.async_engine.begin() as conn:
                    logger.info("🔄 Creating database tables")
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("✅ Tables successfully created")

            except Exception as e:
                logger.error(f"❌ Error occurred: {e}")
                raise


    @staticmethod
    async def check_db_tables() -> bool:
        async with session_manager.async_engine.connect() as conn:

            def _get_existing_tables(conn):
                table_names = inspect(conn).get_table_names()
                system_tables = {"alembic_version"}

                if existing_tables := next(
                    (name for name in table_names if name not in system_tables), None
                ):
                    return existing_tables

            if await conn.run_sync(_get_existing_tables):
                return True
        return False


    @staticmethod
    async def check_connection() -> None:
        async for session in session_manager.get_async_session():
            await session.execute(text("SELECT 1"))



if __name__ == "__main__":
    asyncio.run(DatabaseManager.check_connection())
