from fastapi import APIRouter

from app.core.exceptions import DatabaseConnectionError
from app.utils.db_utils import check_db_connection


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check():
    try:
        await check_db_connection()
    except Exception:
        raise DatabaseConnectionError()
