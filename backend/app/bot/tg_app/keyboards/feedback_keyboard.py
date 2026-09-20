from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

feedback_kb_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выйти из чата',
                          callback_data='chat_exit')]])