from backend.app.core import get_settings

import backend.app.bot.tg_app.keyboards as kb

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

settings = get_settings()

router = Router()

OWNER_ID = settings.owner_id


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(text=f'Привет\n'
                             f'Твой ID: {message.from_user.id}\n'
                             f'Имя: {message.from_user.first_name}',
                        reply_markup=kb.settings)



@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@router.message(F.from_user.id == OWNER_ID,
                F.reply_to_message)
async def reply_to_user(message: Message):
    try:
        user_id = message.reply_to_message.forward_origin.sender_user.id
        await message.bot.send_message(chat_id=user_id,
                                       text=f'Ответ от администратора:\n\n{message.text}')
        await message.reply('Ответ успешно отправлен пользователю')
    except Exception:
        await message.reply('Не удалось отправить ответ')

@router.message(F.text)
async def forward_to_owner(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.forward(chat_id=OWNER_ID)
        await message.answer('Ваше сообщение отправлено успешно')
# @router.message(F.text == 'Как дела?')
# async def how_are_you(message: Message):
#     await message.answer('Все отлично, твои как?')


