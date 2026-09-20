import asyncio

from aiogram import Dispatcher, Bot

from backend.app.bot.tg_app.handlers import router
from backend.app.core import get_settings
from backend.app.data_base import async_session_factory
from backend.app.bot.tg_app.tg_database import DbSessionMiddleWare

settings = get_settings()

BOT = Bot(token=settings.telegram_bot_token)

dp = Dispatcher()
dp.update.middleware(DbSessionMiddleWare(session_factory=async_session_factory))
dp.include_router(router)


async def start_bot():
    retry_delay = 2
    while True:
        try:
            await dp.start_polling(BOT, drop_pending_updates=True)
            break
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
