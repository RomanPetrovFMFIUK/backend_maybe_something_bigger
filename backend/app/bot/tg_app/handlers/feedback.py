import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from backend.app.bot.tg_app.states import FeedbackState
from backend.app.core import get_settings

settings = get_settings()
OWNER_ID = settings.owner_id

router = Router()


@router.message(F.text == 'Связаться с Админом', F.from_user.id != OWNER_ID)
async def ask_for_message(message: Message, state: FSMContext):
    await message.reply('✍️ Введите ваше сообщение:')
    await state.set_state(FeedbackState.waiting_for_message)


@router.message(FeedbackState.waiting_for_message)
async def forward_to_owner(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, отправьте текстовое сообщение')
        return  # ← важно: без return код продолжал выполняться с None

    admin_text = (
        f'📬 У вас новое сообщение!\n'
        f'<b>От:</b> {message.from_user.full_name}\n'
        f'<b>ID:</b> {message.from_user.id}\n\n'
        f'💬 {message.text}'
    )

    await message.bot.send_message(
        chat_id=OWNER_ID,
        text=admin_text,
        parse_mode='HTML',
    )

    await message.answer(
        'Ваше сообщение отправлено!\n'
        'Администратор скоро ответит вам.'
    )
    await state.clear()


@router.message(F.from_user.id == OWNER_ID, F.reply_to_message)
async def reply_to_user(message: Message):
    original_text = message.reply_to_message.text
    if not original_text:
        return

    match = re.search(r'ID:\s*(\d+)', original_text)
    if not match:
        await message.reply('Не смог найти ID пользователя в сообщении')
        return

    user_id = int(match.group(1))
    await message.bot.send_message(
        chat_id=user_id,
        text=f'Ответ от Администратора:\n\n{message.text}',
    )
    await message.reply('Ответ успешно доставлен')
