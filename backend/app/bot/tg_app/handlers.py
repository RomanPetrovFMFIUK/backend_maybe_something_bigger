from backend.app.core import get_settings

import backend.app.bot.tg_app.keyboards as kb

import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

settings = get_settings()

router = Router()

OWNER_ID = settings.owner_id

class FeedbackState(StatesGroup):
    waiting_for_message = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(text=f'Привет\n'
                             f'Твой ID: {message.from_user.id}\n'
                             f'Имя: {message.from_user.first_name}',
                        reply_markup=kb.main)



@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')

@router.message(F.text == 'Связаться с Админом', F.from_user.id != OWNER_ID)
async def ask_for_message(message: Message, state: FSMContext):
    await message.reply('Введите ваше сообщение')
    await state.set_state(FeedbackState.waiting_for_message)


@router.message(F.from_user.id == OWNER_ID,
                F.reply_to_message,)
async def reply_to_user(message: Message):
    original_text = message.reply_to_message.text
    if not original_text:
        return
    match = re.search(r'ID:\s(\d+)', original_text)
    if match:
        user_id = int(match.group(1))
        await message.bot.send_message(chat_id=user_id,
                                       text=f'Ответ от Администратора: \n\n{message.text}')

        await message.reply('Ответ был успешно доставлен')
    else:
        await message.reply('Не смог найти ID пользователя')


@router.message(FeedbackState.waiting_for_message)
async def forward_to_owner(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста отправьте текст')

    admin_text = (
        f'У вас новое сообщение!\n'
        f'{message.from_user.full_name}\n'
        f'ID: {message.from_user.id}\n\n'
        f'Сообщение: {message.text}'
    )

    await message.bot.send_message(
        chat_id=OWNER_ID,
        text=admin_text,
        parse_mode='HTML'
    )

    await message.answer('Ваше сообщение было успешно отправлено!\n'
                         'Администратор в скором времени ответит вам')
    await state.clear()


# @router.message(F.text == 'Как дела?')
# async def how_are_you(message: Message):
#     await message.answer('Все отлично, твои как?')


