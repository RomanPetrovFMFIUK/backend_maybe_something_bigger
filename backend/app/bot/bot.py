# Бот, который будет отправлять владельцу сайта уведомление о том, что зарегистрировался новый пользователь


# Так же с помощью этого бота можно будет связаться с владельцем сайта (Я хочу добавить такую возможность для рядовых пользователей)

# Займусь этим уже завтра

from aiogram import Dispatcher, Bot

from backend.app.bot.tg_app.handlers import router  # агрегированный роутер из handlers/__init__.py
from backend.app.core import get_settings
from backend.app.data_base import async_session_factory
from backend.app.bot.tg_app.tg_database import DbSessionMiddleWare

settings = get_settings()

BOT = Bot(token=settings.telegram_bot_token)

dp = Dispatcher()
dp.update.middleware(DbSessionMiddleWare(session_factory=async_session_factory))
dp.include_router(router)

async def start_bot():
    await dp.start_polling(BOT)