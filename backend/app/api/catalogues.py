from fastapi import APIRouter, Depends

from backend.app.schemas import (CatalogueResponse,
                                 CatalogueCreate,
                                 ProductResponse)

from backend.app.services import CatalogueService, ProductService
from backend.app.dependencies import get_uow, get_current_auth_user
from backend.app.repositories.unit_of_work import UnitOfWork

router = APIRouter(prefix='/catalogues', tags=['Catalogues'])

catalogue_service = CatalogueService()


@router.get('/', response_model=list[CatalogueResponse])
async def get_catalogues(uow: UnitOfWork = Depends(get_uow)) -> list[CatalogueResponse]:
    return await catalogue_service.list_catalogues(uow=uow)


@router.post('/', response_model=CatalogueResponse, dependencies=[Depends(get_current_auth_user)])
async def create_catalogue(catalogue: CatalogueCreate,
                           uow: UnitOfWork = Depends(get_uow)) -> CatalogueResponse:
    return await catalogue_service.create_catalogue(uow=uow, catalogue_create=catalogue)


@router.get('/{catalogue_id}', response_model=CatalogueResponse)
async def get_catalogue(catalogue_id: str,
                        uow: UnitOfWork = Depends(get_uow)) -> CatalogueResponse:
    return await catalogue_service.get_catalogue(uow=uow, catalogue_id=catalogue_id)


@router.delete('/{catalogue_id}', status_code=204, dependencies=[Depends(get_current_auth_user)])
async def delete_catalogue(catalogue_id: str,
                           uow: UnitOfWork = Depends(get_uow)) -> None:
    return await catalogue_service.delete_catalogue(uow=uow, catalogue_id=catalogue_id)


@router.get('/{catalogue_id}/products', response_model=list[ProductResponse])
async def get_products_by_catalogue(catalogue_id: str,
                                    limit: int,
                                    offset: int,
                                    uow: UnitOfWork = Depends(get_uow),
                                    ) -> list[ProductResponse]:
    return await catalogue_service.list_products_by_catalogue_id(uow=uow,
                                                                 catalogue_id=catalogue_id,
                                                                 limit=limit,
                                                                 offset=offset)


@router.post('/{catalogue_id}/products/{product_id}', response_model=ProductResponse,
             dependencies=[Depends(get_current_auth_user)])
async def add_product_from_catalogue(catalogue_id: str, product_id: str,
                                     uow: UnitOfWork = Depends(get_uow)) -> ProductResponse:
    catalogue = await catalogue_service.get_catalogue(uow=uow, catalogue_id=catalogue_id)

    prod_service = ProductService()
    product = await prod_service.get_product(uow=uow, product_id=product_id)
    return await catalogue_service.add_product_to_catalogue(uow=uow, catalogue=catalogue, product=product)


@router.delete('/{catalogue_id}/products/{product_id}', status_code=204, dependencies=[Depends(get_current_auth_user)])
async def delete_product_to_catalogue(catalogue_id: str, product_id: str,
                                      uow: UnitOfWork = Depends(get_uow)):
    prod_service = ProductService()
    catalogue = await catalogue_service.get_catalogue(uow=uow, catalogue_id=catalogue_id)
    product = await prod_service.get_product(uow=uow, product_id=product_id)
    return await catalogue_service.delete_product_from_catalogue(uow=uow, catalogue=catalogue, product=product)
