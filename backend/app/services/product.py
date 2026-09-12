from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories import ProductRepository
from backend.app.schemas import ProductCreate, ProductResponse


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.product_repository = ProductRepository(db=db)

    async def list_products(self) -> list[ProductResponse]:
        products_orm = await self.product_repository.get_all()
        return [ProductResponse.model_validate(product) for product in products_orm]

    async def create_product(self, product_create: ProductCreate) -> ProductResponse:
        product_orm = await self.product_repository.create(name=product_create.name,
                                                           price=product_create.price,
                                                           amount=product_create.amount,
                                                           user_id=product_create.user_id)
        await self.db.commit()
        await self.db.refresh(product_orm)
        return ProductResponse.model_validate(product_orm)

    async def get_product(self, product_id: str) -> ProductResponse:
        product = await self.product_repository.get_by_id(product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Продукт не найден')
        return ProductResponse.model_validate(product)

    async def delete_product(self, product_id: str) -> None:
        product = await self.product_repository.get_by_id(product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Продукт не найден')
        await self.product_repository.delete(product)
        await self.db.commit()