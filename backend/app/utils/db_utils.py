import asyncio

from dotenv import set_key, load_dotenv
from sqlalchemy import inspect, text

from app.utils.create_superuser import create_superuser
from app.core.database import session_manager
from app.core.logging_config import get_logger
from app.entities.base import Base
from app.core.config import settings


logger = get_logger(__name__)


class DatabaseManager():

    @staticmethod
    async def drop_all_tables() -> None:
        try:
            async with session_manager.async_engine.begin() as conn:
                await conn.execute(text("DROP SCHEMA public CASCADE"))
                await conn.execute(text("CREATE SCHEMA public"))
                await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
                await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
            logger.warning("❌ Tables have been dropped")
        except Exception as e:
            logger.error(f"Error during drop_all_tables: {e}")

    @staticmethod
    async def create_db_tables() -> None:
        try:
            async with session_manager.async_engine.begin() as conn:
                logger.info("🔄 Creating database tables")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("✅ Tables successfully created")

        except Exception as e:
            logger.error(f"❌ Error occurred: {e}")
            raise


    #NOTE: temporary unused
    @staticmethod
    async def _check_db_tables() -> bool:
        async with session_manager.async_engine.connect() as conn:

            def _get_existing_tables(conn):
                table_names = inspect(conn).get_table_names()
                system_tables = {"alembic_version"}

                if existing_tables := next((name for name in table_names if name not in system_tables), None):
                    return existing_tables

            if await conn.run_sync(_get_existing_tables):
                return True
        return False


    @staticmethod
    async def check_db_connection() -> None:
        async for session in session_manager.get_async_session():
            await session.execute(text("SELECT 1"))



async def first_run() -> None:
    async def _switch_first_run_variable() -> None:
        set_key(
            quote_mode="never",
            dotenv_path = settings.base.ENV_FILE,
            key_to_set = "FIRST_RUN_VARIABLE",
            value_to_set = "True"
        )

    if settings.base.FIRST_RUN_VARIABLE == False:
        logger.info("🌟 Starting first run setup...")

        await DatabaseManager.create_db_tables()
        await create_superuser() #TODO: move here

        await _switch_first_run_variable()

        logger.info("✅ First run setup completed.")




if __name__ == "__main__":
    asyncio.run(DatabaseManager.check_db_connection())







