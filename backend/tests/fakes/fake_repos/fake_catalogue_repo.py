import uuid

from backend.app.models import (Catalogue,
                                Product)
from backend.tests.fakes.fake_repos.fake_product_repo import FakeProductRepository


class FakeCatalogueRepository:
    def __init__(self,
                 initial_catalogues: list[Catalogue] | None = None,
                 product_repo: FakeProductRepository | None = None) -> None:
        self._catalogues : dict[str, Catalogue] = {}
        self._product_repo = product_repo or FakeProductRepository()
        if initial_catalogues:
            for catalogue in initial_catalogues:
                if not catalogue.id:
                    catalogue.id = str(uuid.uuid4())
                self._catalogues[str(catalogue.id)] = catalogue

    async def get_all_catalogues(self) -> list[Catalogue]:
        return list(self._catalogues.values())

    async def get_catalogue(self, catalogue_id: str) -> Catalogue | None:
        return self._catalogues.get(catalogue_id)

    async def get_products_by_catalogue_id(self,
                                           catalogue_id: str,
                                           limit: int = 15,
                                           offset: int = 0) -> list[Product]:
        catalogue = await self.get_catalogue(catalogue_id)
        if not catalogue or not catalogue.products:
            return []

        return list(catalogue.products)[offset : offset + limit]

    async def create_catalogue(self, catalogue_name) -> Catalogue:
        new_catalogue = Catalogue(name=catalogue_name,
                                  products=[],
                                  id=str(uuid.uuid4()))
        self._catalogues[new_catalogue.id] = new_catalogue
        return new_catalogue

    async def delete_catalogue(self,
                               catalogue: Catalogue) -> None:
        self._catalogues.pop(catalogue.id)

    async def add_product_to_catalogue(self,
                                       product_id: str,
                                       catalogue_id: str) -> None:
        catalogue = await self.get_catalogue(catalogue_id=catalogue_id)
        product = await self._product_repo.get_by_id(product_id=product_id)
        if catalogue and product and product not in catalogue.products:
            catalogue.products.append(product)

    async def delete_product_from_catalogue(self,
                                            product_id: str,
                                            catalogue_id: str) -> None:
        catalogue = await self.get_catalogue(catalogue_id=catalogue_id)
        product = await self._product_repo.get_by_id(product_id=product_id)
        if catalogue and product and product in catalogue.products:
            catalogue.products.remove(product)