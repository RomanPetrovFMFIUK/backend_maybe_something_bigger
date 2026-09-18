from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == 'Каталог')
async def show_catalogue(message: Message):
    # TODO: подключить DatabaseMiddleware и получать данные из БД
    await message.answer('📦 Каталог пока пуст')
