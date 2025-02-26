from typing import AsyncGenerator
import asyncio

from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import inspect, text
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings
from app.core.logging_config import logger


class Base(DeclarativeBase):
    __abstract__ = True


class DatabaseManager:

    def __init__(self):
        self.logger = logger

        self.async_engine = create_async_engine(
            settings.database.async_db_url,
            future=True,
        )

        self.AsyncSessionFactory = async_sessionmaker(
            bind=self.async_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
   
    @staticmethod
    def _after_retry(retry_state):
        attempt = retry_state.attempt_number
        if retry_state.outcome.failed:
            logger.warning(
                f"❌ Попытка {attempt}: Ошибка подключения к БД, повторяем..."
            )
        else:
            logger.info(f"✅ Попытка {attempt}: Подключение успешно.")

    @retry(
        stop=stop_after_attempt(settings.tenacity.MAX_TRIES),
        wait=wait_fixed(settings.tenacity.WAIT_SECONDS),
        after=_after_retry,
    )
    async def check_db_connection(self) -> None:
        try:
            async with self.AsyncSessionFactory() as db:
                await db.execute(text("SELECT 1"))
        except Exception as e:
            self.logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionFactory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def drop_all_tables(self):
        async with self.async_engine.begin() as db:
            await db.execute(text("DROP SCHEMA public CASCADE"))
            await db.execute(text("CREATE SCHEMA public"))
            await db.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            await db.execute(text("GRANT ALL ON SCHEMA public TO public"))
            self.logger.warning("❌ Таблицы удалены")


    async def create_tables_if_not_exist(self):
        async with self.async_engine.begin() as db:

            def check_tables(conn):
                inspector = inspect(conn)
                tables = inspector.get_table_names()
                system_tables = {"alembic_version"}

                return [t for t in tables if t not in system_tables]

            if not (_ := await db.run_sync(check_tables)):
                self.logger.info("🔄 Создание таблиц БД")
                await db.run_sync(Base.metadata.create_all)
                self.logger.info("✅ Таблицы успешно созданны")


db_manager = DatabaseManager()
