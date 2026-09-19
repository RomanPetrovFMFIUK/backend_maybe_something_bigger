from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Catalogue, Product, product_catalogue_assoc


class CatalogueRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_catalogues(self) -> list[Catalogue]:
        stmt = select(Catalogue).options(selectinload(Catalogue.products))
        catalogues = await self.db.scalars(stmt)
        return list(catalogues.all())

    async def get_catalogue(self, catalogue_id: str) -> Catalogue | None:
        stmt = select(Catalogue).options(selectinload(Catalogue.products)).where(Catalogue.id == catalogue_id)
        catalogue = await self.db.scalar(stmt)
        return catalogue

    async def get_products_by_catalogue_id(self, catalogue_id: str) -> list[Product]:
        stmt = (
            select(Product)
            .join(Product.catalogues)
            .where(Catalogue.id == catalogue_id)
        )
        products = await self.db.scalars(stmt)
        return list(products.all())

    async def create_catalogue(self, catalogue_name: str) -> Catalogue:
        new_catalogue = Catalogue(name=catalogue_name,
                                  products=[])
        self.db.add(new_catalogue)
        return new_catalogue

    async def delete_catalogue(self, catalogue: Catalogue) -> None:
        await self.db.delete(catalogue)


# Добавляем наш объект в ассоциативную таблицу
    async def add_product_to_catalogue(self, product_id: str, catalogue_id: str) -> None:
        stmt = insert(product_catalogue_assoc).values(
            product_id=product_id,
            catalogue_id=catalogue_id
        )
        await self.db.execute(stmt)

# Удаляем наш объект из ассоциативной таблицы
    async def delete_product_from_catalogue(self, product_id: str, catalogue_id: str) -> None:
        stmt = delete(product_catalogue_assoc).where(
            product_catalogue_assoc.c.product_id == product_id,
            product_catalogue_assoc.c.catalogue_id == catalogue_id
        )
        await self.db.execute(stmt)
