from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from backend.app.bot.tg_app.keyboards import main_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        text=(
            f'Привет!\n'
            f'Твой ID: {message.from_user.id}\n'
            f'Имя: {message.from_user.first_name}'
        ),
        reply_markup=main_kb,
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '/start — главное меню\n'
        '/help — эта справка\n'
        '/about_us - информация про нас\n'
    )

@router.message(Command('about_us'))
async def cmd_about_us(message: Message):
    await message.answer(text='Это мой пет-проект, который в будещем'
                              ' возможно разрастеться во что то большее')

