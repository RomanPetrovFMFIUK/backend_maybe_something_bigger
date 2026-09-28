from types import TracebackType

from .fake_user_repository import FakeUserRepository
from .fake_product_repo import FakeProductRepository
from .fake_catalogue_repo import FakeCatalogueRepository



class FakeUnitOfWork:
    def __init__(self):
        self.users = FakeUserRepository()
        self.products = FakeProductRepository()
        self.catalogues = FakeCatalogueRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ):
        if exc_type is not None:
            await self.rollback()

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True
