from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse

from backend.core.config import settings
from backend.core.database import session_manager
from backend.core.logging_config import get_logger
from backend.core.managers import DatabaseManager, ImportManager
from fake.main import Seeder

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.base.ENVIRONMENT == "local":
        await DatabaseManager.drop_all_tables()  # WARN: REMOVE THIS!

        if not await DatabaseManager.check_db_tables():
            await DatabaseManager.create_db_tables()
            await Seeder.seed_all()

    ImportManager.import_routers(app)
    yield

    await session_manager.dispose()


app = FastAPI(
    title=settings.base.BACKEND_APP_NAME,
    version=settings.base.BACKEND_APP_VERSION,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)


@app.exception_handler(Exception)
async def exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Что-то пошло не так!", "error": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
