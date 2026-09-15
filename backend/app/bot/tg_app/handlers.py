import backend.app.bot.tg_app.keyboards as kb

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(text=f'Привет\n'
                             f'Твой ID: {message.from_user.id}\n'
                             f'Имя: {message.from_user.first_name}',
                        reply_markup=kb.settings)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')



# @router.message(F.text == 'Как дела?')
# async def how_are_you(message: Message):
#     await message.answer('Все отлично, твои как?')


