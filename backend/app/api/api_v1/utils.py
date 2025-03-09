from fastapi import APIRouter

from app.core.logging_config import get_logger
from app.core.exceptions import DatabaseConnectionError
from app.utils.db_utils import DatabaseManager


logger = get_logger(__name__)
router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check():
    try:
        await DatabaseManager.check_db_connection()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseConnectionError()
