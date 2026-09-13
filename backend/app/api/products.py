from fastapi import APIRouter, Depends

from backend.app.schemas import ProductCreate, ProductResponse
from backend.app.services import ProductService
from backend.app.dependencies import get_current_auth_user, get_uow
from backend.app.repositories.unit_of_work import UnitOfWork

router = APIRouter(prefix='/products', tags=['Products'])

product_service = ProductService()

@router.get('/', response_model=list[ProductResponse])
async def get_products(uow: UnitOfWork = Depends(get_uow)) -> list[ProductResponse]:
    return await product_service.list_products(uow=uow)


@router.post('/', response_model=ProductResponse, dependencies=[Depends(get_current_auth_user)])
async def create_product(product: ProductCreate,
                         uow: UnitOfWork = Depends(get_uow)) -> ProductResponse:
    return await product_service.create_product(uow=uow, product_create=product)


@router.get('/{product_id}', response_model=ProductResponse)
async def get_product(product_id: str,
                      uow: UnitOfWork = Depends(get_uow)) -> ProductResponse:
    return await product_service.get_product(uow=uow, product_id=product_id)


@router.delete('/{product_id}', status_code=204, dependencies=[Depends(get_current_auth_user)])
async def delete_product(product_id: str,
                         uow: UnitOfWork = Depends(get_uow)) -> None:
    return await product_service.delete_product(uow=uow, product_id=product_id)
