from app.core.logging_config import logger
from app.core.database import db_manager
import asyncio


async def main() -> None:
    logger.info("Initializing service")
    await db_manager.check_db_connection()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
