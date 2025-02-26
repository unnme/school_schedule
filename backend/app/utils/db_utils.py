from app.core.database import db_manager
import asyncio


async def main() -> None:

    await db_manager.check_db_connection()



if __name__ == "__main__":
    asyncio.run(main())
