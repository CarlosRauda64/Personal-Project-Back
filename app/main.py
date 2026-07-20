from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra los modelos en SQLModel.metadata)
from app.api import home
from app.api.v1.router import api_router
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_db_and_tables()
    yield


app = FastAPI(
    title="Personal Project API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(home.router)
app.include_router(api_router, prefix="/api/v1")
