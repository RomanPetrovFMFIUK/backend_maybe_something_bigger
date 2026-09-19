from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.bot.tg_app.keyboards import inline_catalogues

from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == 'Каталог')
async def show_catalogues(message: Message, session: AsyncSession):
    await message.reply('Привет, это наш каталог\n',
                        reply_markup=await inline_catalogues(session=session))
