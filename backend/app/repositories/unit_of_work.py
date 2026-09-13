from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories import (CatalogueRepository,
                          ProductRepository,
                          UserRepository)

from types import TracebackType


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.catalogues = CatalogueRepository(session)
        self.products = ProductRepository(session)
        self.users = UserRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None,
                        exc_val: BaseException | None,
                        exc_tb: TracebackType | None):
        if exc_type is not None:
            await self.session.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()