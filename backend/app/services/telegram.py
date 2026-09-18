from aiogram import Router, Bot
from backend.app.core import get_settings
from backend.app.schemas import UserResponse

settings = get_settings()

OWNER_ID = settings.owner_id

router = Router()


class TelegramService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_message_about_new_user(self, user: UserResponse):
        text = (
            f"Зарегистрировался новый пользователь\n"
            f"Имя и Фамилия: {user.full_name}\n"
            f"Возраст пользователя: {user.age}\n"
            f"Админ: {user.admin}"
        )

        await self.bot.send_message(
            chat_id=OWNER_ID,
            text=text,
            parse_mode='HTML'
        )




