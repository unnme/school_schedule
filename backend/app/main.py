from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.utils.router_manager import import_routers
from app.utils.db_utils import create_tables_if_not_exist, drop_all_tables
from app.utils.create_superuser import create_superuser
from app.core.database import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_all_tables()
    # await create_tables_if_not_exist()
    # await create_superuser()

    yield

    await session_manager.dispose()


app = FastAPI(
    title=settings.base.PROJECT_NAME,
    description="...",
    version=settings.base.PROJECT_VERSION,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import_routers(app)
