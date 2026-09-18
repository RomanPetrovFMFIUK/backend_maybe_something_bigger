import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.api import router
from backend.app.core import get_settings
from backend.app.data_base import engine
from backend.app.models import Base
from backend.app.bot.bot import BOT, start_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    polling_task = asyncio.create_task(start_bot())
    yield
    polling_task.cancel()
    await bot.session.close()
    await engine.dispose()


settings = get_settings()

app = FastAPI(title="Asynchronost", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
