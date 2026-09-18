from fastapi import HTTPException

from aiogram import Router, F
from aiogram.types import Message

from backend.app.core import get_settings

settings = get_settings()

OWNER_ID = settings.owner_id

router = Router()


class TelegramService:
    @router.message()
    async def send_message_about_new_user(self,
                                          message: Message
                                          ):



