from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.app.core import get_settings

settings = get_settings()

engine = create_async_engine(
    url=settings.DB_URL,
    echo=settings.DB_ECHO,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db():
    async with async_session_factory() as session:
        yield session
