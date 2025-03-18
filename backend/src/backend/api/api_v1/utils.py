from fastapi import APIRouter

from backend.core.exceptions import DatabaseConnectionError
from backend.core.logging_config import get_logger
from backend.utils.db_utils import DatabaseManager

logger = get_logger(__name__)
router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check():
    try:
        await DatabaseManager.check_db_connection()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()


# @router.get("/some-check/") #BUG:
# async def some_check():
#     print(
#         Base.metadata.sorted_tables
#     )
