from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import backend.app.bot.tg_app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        text=(
            f'Привет!\n'
            f'Твой ID: {message.from_user.id}\n'
            f'Имя: {message.from_user.first_name}'
        ),
        reply_markup=kb.main,
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '❓ Доступные команды:\n'
        '/start — главное меню\n'
        '/help — эта справка'
    )
