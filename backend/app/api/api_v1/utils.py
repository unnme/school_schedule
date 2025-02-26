from fastapi import APIRouter

from app.core.database import db_manager


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check() -> bool:
    await db_manager.check_db_connection()

    return True
