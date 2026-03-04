from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.db.session import async_get_adb, engine
from app.main import app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """Recreate tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db(setup_db: None) -> AsyncGenerator[AsyncSession, None]:
    """Explicitly depends on setup_db to guarantee table creation order."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


@pytest_asyncio.fixture()
async def aclient(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[async_get_adb] = lambda: (yield db)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1") as aclient:
        yield aclient
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"
