# Бот, который будет отправлять владельцу сайта уведомление о том, что зарегистрировался новый пользователь


# Так же с помощью этого бота можно будет связаться с владельцем сайта (Я хочу добавить такую возможность для рядовых пользователей)

# Займусь этим уже завтра

from aiogram import Dispatcher, Bot

from backend.app.bot.tg_app.handlers import router
from backend.app.bot.config import TOKEN

import logging
import asyncio

bot = Bot(token=TOKEN)

dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
