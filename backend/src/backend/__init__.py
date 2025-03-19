from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse

from backend.core.config import settings
from backend.core.database import session_manager
from backend.core.logging_config import get_logger
from backend.core.router_manager import import_routers
from backend.utils.db_utils import first_run

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await first_run()
    import_routers(app)
    yield

    await session_manager.dispose()


app = FastAPI(
    title=settings.base.PROJECT_NAME,
    version=settings.base.PROJECT_VERSION,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
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
