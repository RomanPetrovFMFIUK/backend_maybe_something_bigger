from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories import CatalogueRepository
from backend.app.schemas import CatalogueCreate, CatalogueResponse, ProductResponse


class CatalogueService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.catalogue_repository = CatalogueRepository(db=db)

    async def get_catalogue(self, catalogue_id: str) -> CatalogueResponse:
        catalogue = await self.catalogue_repository.get_catalogue(catalogue_id)
        return CatalogueResponse.model_validate(catalogue)

    async def list_catalogues(self) -> list[CatalogueResponse]:
        catalogues_orm = await self.catalogue_repository.get_all_catalogues()
        return [CatalogueResponse.model_validate(catalogue) for catalogue in catalogues_orm]

    async def list_products_by_catalogue_id(self, catalogue_id: str) -> list[ProductResponse]:
        products_orm = await self.catalogue_repository.get_products_by_catalogue_id(catalogue_id=catalogue_id)
        return [ProductResponse.model_validate(product) for product in products_orm]

    async def list_products_by_catalogue_name(self, catalogue_name: str) -> list[ProductResponse]:
        products_orm = await self.catalogue_repository.get_products_by_catalogue_name(catalogue_name=catalogue_name)
        return [ProductResponse.model_validate(product) for product in products_orm]

    async def create_catalogue(self, catalogue_create: CatalogueCreate) -> CatalogueResponse:
        new_catalogue = await self.catalogue_repository.create_catalogue(catalogue_name=catalogue_create.name)
        await self.db.commit()
        await self.db.refresh(new_catalogue)
        return CatalogueResponse.model_validate(new_catalogue)

    async def delete_catalogue(self, catalogue_id: str) -> None:
        catalogue_to_delete = await self.catalogue_repository.get_catalogue(catalogue_id)
        if not catalogue_to_delete:
            raise HTTPException(status_code=404, detail='Каталог не найден')
        await self.catalogue_repository.delete_catalogue(catalogue_to_delete)
        await self.db.commit()

    async def add_product_to_catalogue(self,
                                       product: ProductResponse,
                                       catalogue: CatalogueResponse) -> ProductResponse:
        await self.catalogue_repository.add_product_to_catalogue(
            product_id=product.id,
            catalogue_id=catalogue.id
        )
        await self.db.commit()
        return ProductResponse.model_validate(product)

    async def delete_product_from_catalogue(self,
                                            product: ProductResponse,
                                            catalogue: CatalogueResponse) -> None:
        await self.catalogue_repository.delete_product_from_catalogue(
            product_id=product.id,
            catalogue_id=catalogue.id
        )
        await self.db.commit()
