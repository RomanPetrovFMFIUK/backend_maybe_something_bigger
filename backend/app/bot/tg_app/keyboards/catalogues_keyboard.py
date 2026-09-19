from backend.app.repositories import UnitOfWork
from backend.app.services import CatalogueService

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession


catalogue_service = CatalogueService()

async def inline_catalogues(session: AsyncSession):
    uow = UnitOfWork(session=session)
    catalogues = await catalogue_service.list_catalogues(uow=uow)
    catalogues_kb = InlineKeyboardBuilder()
    for catalogue in catalogues:
        catalogues_kb.add(InlineKeyboardButton(text=catalogue.name,
                                               callback_data="some_action"))
    return catalogues_kb.adjust(2).as_markup()

