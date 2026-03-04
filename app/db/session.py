"""database configuration async."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import config

engine = create_async_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in (config.DATABASE_URL or "") else {},
)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def async_get_adb() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session and close it after use."""
    async with AsyncSessionLocal() as session:
        yield session
