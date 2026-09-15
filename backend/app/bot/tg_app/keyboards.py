from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           WebAppInfo)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'),
     KeyboardButton(text='Связаться с Админом')],
    [KeyboardButton(text='Перейти на веб-страницу')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню')

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наш сайт: ',
                          url='https://svit-line.com.ua/ua/index.html')]
])

