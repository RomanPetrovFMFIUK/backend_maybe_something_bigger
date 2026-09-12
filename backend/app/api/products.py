from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.data_base import get_db
from backend.app.schemas import ProductCreate, ProductResponse
from backend.app.services import ProductService
from backend.dependencies import get_current_auth_user

router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/', response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)) -> list[ProductResponse]:
    service = ProductService(db=db)
    return await service.list_products()


@router.post('/', response_model=ProductResponse, dependencies=[Depends(get_current_auth_user)])
async def create_product(product: ProductCreate,
                         db: AsyncSession = Depends(get_db)) -> ProductResponse:
    service = ProductService(db=db)
    return await service.create_product(product_create=product)


@router.get('/{product_id}', response_model=ProductResponse)
async def get_product(product_id: str,
                      db: AsyncSession = Depends(get_db)) -> ProductResponse:
    service = ProductService(db=db)
    return await service.get_product(product_id=product_id)


@router.delete('/{product_id}', status_code=204, dependencies=[Depends(get_current_auth_user)])
async def delete_product(product_id: str,
                         db: AsyncSession = Depends(get_db)) -> None:
    service = ProductService(db=db)
    return await service.delete_product(product_id=product_id)
