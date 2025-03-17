from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from rich.console import Console

from src.core.config import settings
from src.core.database import session_manager
from src.core.router_manager import import_routers
from src.utils.db_utils import first_run


@asynccontextmanager
async def lifespan(app: FastAPI):
    await first_run()
    import_routers(app)
    yield

    await session_manager.dispose()


app = FastAPI(
    title=settings.base.PROJECT_NAME,
    description="...",
    version=settings.base.PROJECT_VERSION,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

console = Console(force_terminal=True)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    console.print_exception(show_locals=True)
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


