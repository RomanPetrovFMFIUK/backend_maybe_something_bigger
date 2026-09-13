from fastapi import HTTPException
from backend.app.schemas import ProductCreate, ProductResponse


class ProductService:
    async def list_products(self, uow) -> list[ProductResponse]:
        async with uow:
            products_orm = await uow.products.get_all()
            return [ProductResponse.model_validate(product) for product in products_orm]

    async def create_product(self, uow, product_create: ProductCreate) -> ProductResponse:
        async with uow:
            product_orm = await uow.products.create(name=product_create.name,
                                                    price=product_create.price,
                                                    amount=product_create.amount,
                                                    user_id=product_create.user_id)
            await uow.commit()
            await uow.session.refresh(product_orm)
            return ProductResponse.model_validate(product_orm)

    async def get_product(self, uow, product_id: str) -> ProductResponse:
        async with uow:
            product = await uow.products.get_by_id(product_id=product_id)
            if not product:
                raise HTTPException(status_code=404, detail='Продукт не найден')
            return ProductResponse.model_validate(product)

    async def delete_product(self, uow, product_id: str) -> None:
        async with uow:
            product = await uow.products.get_by_id(product_id=product_id)
            if not product:
                raise HTTPException(status_code=404, detail='Продукт не найден')
            await uow.products.delete(product)
            await uow.commit()