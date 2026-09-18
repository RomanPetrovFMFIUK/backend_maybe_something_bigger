from aiogram import Router

from backend.app.bot.tg_app.handlers.common import router as common_router
from backend.app.bot.tg_app.handlers.feedback import router as feedback_router
from backend.app.bot.tg_app.handlers.catalogue import router as catalogue_router

# Главный роутер — агрегирует все дочерние
router = Router()
router.include_router(common_router)
router.include_router(feedback_router)
router.include_router(catalogue_router)
