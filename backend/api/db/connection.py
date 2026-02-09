from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from config import get_settings

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        settings = get_settings()
        url = settings.database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        _engine = create_async_engine(url, pool_pre_ping=True)
    return _engine
