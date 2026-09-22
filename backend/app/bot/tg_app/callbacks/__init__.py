from aiogram import Router

from .feedback_callbacks import router as feedback_callback_router

callback_router  = Router()
callback_router.include_router(feedback_callback_router)
