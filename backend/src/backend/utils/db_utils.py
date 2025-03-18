import asyncio

from sqlalchemy import inspect, text

from backend.core.database import session_manager
from backend.core.logging_config import get_logger
from backend.entities.base import Base

logger = get_logger(__name__)


class DatabaseManager:
    @staticmethod
    async def _drop_all_tables() -> None:
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
    async def check_db_connection() -> None:
        async for session in session_manager.get_async_session():
            await session.execute(text("SELECT 1"))


async def first_run() -> None:
    # await DatabaseManager._drop_all_tables()  # WARN: REMOVE THIS!

    if not await DatabaseManager.check_db_tables():
        logger.info("🌟 Starting first run setup...")

        await DatabaseManager.create_db_tables()

        logger.info("✅ First run setup completed.")


if __name__ == "__main__":
    asyncio.run(DatabaseManager.check_db_connection())
