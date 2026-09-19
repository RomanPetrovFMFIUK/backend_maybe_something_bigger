from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           )

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'),
     KeyboardButton(text='Связаться с Админом')],
    [KeyboardButton(text='Перейти на веб-страницу')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню')

