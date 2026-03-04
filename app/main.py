"""the main app."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.api.ticket import router as ticket_router
from app.core.logging import configure_logging
from app.db.base import metadata
from app.db.session import AsyncSessionLocal, engine
from app.exceptions.http import http_exception_handler_logging
from app.middlewares.setup import register_middlewares  # noqa: E402

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Session], None]:
    """Handle application startup and shutdown."""
    configure_logging()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    async with AsyncSessionLocal() as db:
        yield {"db": db}
    await engine.dispose()


app = FastAPI(
    title="Tickets Management API",
    description="REST API for ticket management built with FastAPI and SQLAlchemy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)
# Exceptions handlers
app.add_exception_handler(HTTPException, http_exception_handler_logging)

# Routing
app.include_router(ticket_router)

# Middlewares
register_middlewares(app)
