from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import db_manager
from app.core.settings import settings
from app.utils.router_manager import import_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.check_db_connection()
    await db_manager.create_tables_if_not_exist()

    yield


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
