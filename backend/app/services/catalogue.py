from fastapi import HTTPException

from backend.app.repositories import UnitOfWork
from backend.app.schemas import CatalogueCreate, CatalogueResponse, ProductResponse


class CatalogueService:

    async def get_catalogue(self, uow: UnitOfWork, catalogue_id: str) -> CatalogueResponse:
        async with uow:
            catalogue = await uow.catalogues.get_catalogue(catalogue_id)
            return CatalogueResponse.model_validate(catalogue)

    async def list_catalogues(self, uow: UnitOfWork) -> list[CatalogueResponse]:
        async with uow:
            catalogues_orm = await uow.catalogues.get_all_catalogues()
            return [CatalogueResponse.model_validate(catalogue) for catalogue in catalogues_orm]

    async def list_products_by_catalogue_id(self, uow: UnitOfWork, catalogue_id: str) -> list[ProductResponse]:
        async with uow:
            products_orm = await uow.catalogues.get_products_by_catalogue_id(catalogue_id=catalogue_id)
            return [ProductResponse.model_validate(product) for product in products_orm]

    async def list_products_by_catalogue_name(self, uow: UnitOfWork, catalogue_name: str) -> list[ProductResponse]:
        async with uow:
            products_orm = await uow.catalogues.get_products_by_catalogue_name(catalogue_name=catalogue_name)
            return [ProductResponse.model_validate(product) for product in products_orm]

    async def create_catalogue(self, uow: UnitOfWork, catalogue_create: CatalogueCreate) -> CatalogueResponse:
        async with uow:
            new_catalogue = await uow.catalogues.create_catalogue(catalogue_name=catalogue_create.name)
            await uow.commit()
            await uow.session.refresh(new_catalogue)
            return CatalogueResponse.model_validate(new_catalogue)

    async def delete_catalogue(self, uow: UnitOfWork, catalogue_id: str) -> None:
        async with uow:
            catalogue_to_delete = await uow.catalogues.get_catalogue(catalogue_id)
            if not catalogue_to_delete:
                raise HTTPException(status_code=404, detail='Каталог не найден')
            await uow.catalogues.delete_catalogue(catalogue_to_delete)
            await uow.commit()

    async def add_product_to_catalogue(self,
                                       uow: UnitOfWork,
                                       product: ProductResponse,
                                       catalogue: CatalogueResponse) -> ProductResponse:
        async with uow:
            await uow.catalogues.add_product_to_catalogue(
                product_id=product.id,
                catalogue_id=catalogue.id
            )
            await uow.commit()
            return ProductResponse.model_validate(product)

    async def delete_product_from_catalogue(self,
                                            uow: UnitOfWork,
                                            product: ProductResponse,
                                            catalogue: CatalogueResponse) -> None:
        async with uow:
            await uow.catalogues.delete_product_from_catalogue(
                product_id=product.id,
                catalogue_id=catalogue.id
            )
            await uow.commit()
