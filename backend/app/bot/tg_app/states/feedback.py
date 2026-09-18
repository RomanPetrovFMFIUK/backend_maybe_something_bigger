from aiogram.fsm.state import StatesGroup, State


class FeedbackState(StatesGroup):
    waiting_for_message = State()
