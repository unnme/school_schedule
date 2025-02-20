from typing import AsyncGenerator, Generator

from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.settings import settings
from app.core.logging_config import logger

def camel_case_to_snake_case(name: str) -> str:
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

class Base(DeclarativeBase):
    __abstract__= True

    # metadata = MetaData(naming_convention=...)

class DatabaseManager:

    MAX_TRIES = 60 * 5  # 5 минут
    WAIT_SECONDS = 10  # Время ожидания между попытками

    def __init__(self):
        self.async_engine = create_async_engine(
            settings.database.async_db_url,
            echo=settings.database.DB_ECHO,
            future=True,
        )

        self.sync_engine = create_engine(
            settings.database.sync_db_url,
            echo=settings.database.DB_ECHO,
            future=True,
        )

        self.AsyncSessionFactory = async_sessionmaker(
            bind=self.async_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        self.SyncSessionFactory = sessionmaker(
            bind=self.sync_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        self.logger = logger

    @staticmethod
    def _before_retry(retry_state):
        attempt = retry_state.attempt_number
        logger.info(f"🔄 Попытка {attempt}: Проверяем подключение к базе данных...")

    @staticmethod
    def _after_retry(retry_state):
        attempt = retry_state.attempt_number
        if retry_state.outcome.failed:
            logger.warning(f"❌ Попытка {attempt}: Ошибка подключения к БД, повторяем...")
        else:
            logger.info(f"✅ Попытка {attempt}: Подключение успешно.")

    @retry(
        stop=stop_after_attempt(MAX_TRIES),
        wait=wait_fixed(WAIT_SECONDS),
        before=_before_retry,
        after=_after_retry,
    )
    async def check_db_connection(self) -> None:
        try:
            async with self.AsyncSessionFactory() as db:
                await db.execute(text("SELECT 1"))
                self.logger.info("✅ Подключение успешно.")
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

    def get_sync_session(self) -> Generator[Session, None, None]:
        with self.SyncSessionFactory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    async def drop_all_tables(self):
        async with self.async_engine.begin() as db:
            await db.execute(text("DROP SCHEMA public CASCADE"))
            await db.execute(text("CREATE SCHEMA public"))
            await db.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            await db.execute(text("GRANT ALL ON SCHEMA public TO public"))

    async def create_tables(self):
        async with self.async_engine.begin() as db:
            await db.run_sync(Base.metadata.create_all)


db_manager = DatabaseManager()
