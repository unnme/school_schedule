import logging
import asyncio

from sqlalchemy import text, inspect

from app.core.database import session_manager, Base


logger = logging.getLogger(__name__)


async def drop_all_tables():
    async with session_manager.async_engine.begin() as db:
        await db.execute(text("DROP SCHEMA public CASCADE"))
        await db.execute(text("CREATE SCHEMA public"))
        await db.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
        await db.execute(text("GRANT ALL ON SCHEMA public TO public"))
        logger.warning("❌ Таблицы удалены")


async def create_tables_if_not_exist():
    async with session_manager.async_engine.begin() as db:

        def check_tables(conn):
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            system_tables = {"alembic_version"}

            return [t for t in tables if t not in system_tables]

        if not (_ := await db.run_sync(check_tables)):
            logger.info("🔄 Создание таблиц БД")
            await db.run_sync(Base.metadata.create_all)
            logger.info("✅ Таблицы успешно созданны")


async def check_db_connection():
    try:
        async with session_manager.AsyncSessionFactory() as db:
            await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"❌ База данных недоступна {e}")
        raise


if __name__ == "__main__":
    asyncio.run(check_db_connection())
