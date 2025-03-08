import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.utils.create_superuser import create_superuser
from app.core.database import session_manager
from app.core.logging_config import get_logger
from app.entities.base import Base


logger = get_logger(__name__)


async def drop_all_tables():
    try:
        async for conn in session_manager.get_async_session():

            await conn.execute(text("DROP SCHEMA public CASCADE"))
            await conn.execute(text("CREATE SCHEMA public"))
            await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        logger.warning("❌ Tables have been dropped")
    except Exception as e:
        logger.error(f"Error during drop_all_tables: {e}")


async def create_tables_if_not_exist():

    async with session_manager.async_engine.begin() as conn: 

        logger.info("🔄 Creating database tables")

        await conn.execute(
            text("""
                CREATE TABLE service_table (
                    id SERIAL PRIMARY KEY,
                    create_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL UNIQUE
                );
            """)
        )

        logger.info("✅ Service table created")

        await conn.execute(
            text("""
                INSERT INTO service_table (status)
                VALUES (:status)
            """), {"status": "active"}
        )

        await conn.run_sync(Base.metadata.create_all)

        logger.info("✅ Tables successfully created")


async def check_db_entry():
    async for conn in session_manager.get_async_session():

        stmt = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_name = 'service_table';")
        )
        if stmt.fetchone():
            return True


async def check_db_connection():
    async for session in session_manager.get_async_session():
        await session.execute(text("SELECT 1"))


async def run_once():
    if not await check_db_entry():
        await create_tables_if_not_exist()
        await create_superuser()



if __name__ == "__main__":
    asyncio.run(check_db_connection())
