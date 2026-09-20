from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.app.bot.tg_app.states import FeedbackState

router = Router()

@router.callback_query(F.data == 'chat_exit',
                       FeedbackState.waiting_for_message)
async def chat_exit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Вы успешно вышли из чата')
    await state.clear()
    await callback.answer()