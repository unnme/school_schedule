from typing import AsyncGenerator

from sqlalchemy import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.logging_config import get_logger


logger = get_logger(__name__)


class SessionManager:
    def __init__(self):
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

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionFactory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.exception(f"Database error: {e}")
                await session.rollback()
                raise

    async def dispose(self) -> None:
        await self.async_engine.dispose()


session_manager = SessionManager()
