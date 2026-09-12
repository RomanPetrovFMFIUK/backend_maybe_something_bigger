from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import Product

class ProductRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[Product]:
        result = await self.db.execute(select(Product))
        return list(result.scalars().all())

    async def get_by_id(self, product_id: str) -> Product | None:
        return await self.db.get(Product, product_id)

    async def create(self, name: str,
                     price: int,
                     amount: int,
                     user_id: str) -> Product:
        new_product = Product(name=name, price=price, amount=amount, user_id=user_id)
        self.db.add(new_product)
        return new_product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)