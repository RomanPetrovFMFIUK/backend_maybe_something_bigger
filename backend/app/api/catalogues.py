from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.data_base import get_db
from backend.app.schemas import CatalogueResponse, CatalogueCreate, ProductResponse
from backend.app.services import CatalogueService, ProductService

router = APIRouter(prefix='/catalogues', tags=['Catalogues'])


@router.get('/', response_model=list[CatalogueResponse])
async def get_catalogues(db: AsyncSession = Depends(get_db)) -> list[CatalogueResponse]:
    service = CatalogueService(db=db)
    return await service.list_catalogues()


@router.post('/', response_model=CatalogueResponse)
async def create_catalogue(catalogue: CatalogueCreate,
                           db: AsyncSession = Depends(get_db)) -> CatalogueResponse:
    service = CatalogueService(db=db)
    return await service.create_catalogue(catalogue_create=catalogue)


@router.get('/{catalogue_id}', response_model=CatalogueResponse)
async def get_catalogue(catalogue_id: str,
                  db: AsyncSession = Depends(get_db)) -> CatalogueResponse:
    service = CatalogueService(db=db)
    return await service.get_catalogue(catalogue_id=catalogue_id)


@router.delete('/{catalogue_id}', status_code=204)
async def delete_catalogue(catalogue_id: str,
                     db: AsyncSession = Depends(get_db)) -> None:
    service = CatalogueService(db=db)
    return await service.delete_catalogue(catalogue_id=catalogue_id)


@router.get('/{catalogue_id}/products', response_model=list[ProductResponse])
async def get_products_by_catalogue(catalogue_id: str, db: AsyncSession = Depends(get_db)) -> list[ProductResponse]:
    service = CatalogueService(db=db)
    return await service.list_products_by_catalogue_id(catalogue_id=catalogue_id)


@router.post('/{catalogue_id}/products/{product_id}', response_model=ProductResponse)
async def add_product_from_catalogue(catalogue_id: str, product_id: str,
                                  db: AsyncSession = Depends(get_db)) -> ProductResponse:
    cat_service = CatalogueService(db=db)
    prod_service = ProductService(db=db)

    catalogue = await cat_service.get_catalogue(catalogue_id=catalogue_id)
    product = await prod_service.get_product(product_id=product_id)
    return await cat_service.add_product_to_catalogue(catalogue=catalogue, product=product)

@router.delete('/{catalogue_id}/products/{product_id}', status_code=204)
async def delete_product_to_catalogue(catalogue_id: str, product_id: str,
                             db: AsyncSession = Depends(get_db)):
    cat_service = CatalogueService(db=db)
    prod_service = ProductService(db=db)

    catalogue = await cat_service.get_catalogue(catalogue_id=catalogue_id)
    product = await prod_service.get_product(product_id=product_id)
    return await cat_service.delete_product_from_catalogue(catalogue=catalogue, product=product)
