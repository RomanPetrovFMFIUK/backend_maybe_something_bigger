import pytest

from fastapi import HTTPException

from backend.app.schemas import (ProductResponse,
                                 ProductCreate)


async def test_list_product_empty(uow, product_service):
    products = await product_service.list_products(uow=uow)
    assert products == []


async def test_create_product(uow, product_service):
    product_create = ProductCreate(name='some_prod',
                                   price=123,
                                   amount=10,
                                   user_id='some_id')
    product = await product_service.create_product(uow, product_create)
    assert product.name == 'some_prod'
    assert product.price == 123
    assert product.amount == 10


async def test_get_product_found(uow, product_service):
    product_create = ProductCreate(name='some_prod',
                                   price=123,
                                   amount=10,
                                   user_id='some_id')
    product_response = await product_service.create_product(uow, product_create)
    product = await product_service.get_product(uow, product_response.id)
    assert product is not None
    assert product.price == 123
    assert product.name == 'some_prod'
    assert product.amount == 10


async def test_delete_product_success_and_not_found(uow, product_service):
    product_create = ProductCreate(name='some_prod',
                                   price=123,
                                   amount=10,
                                   user_id='some_id')
    product_response = await product_service.create_product(uow, product_create)
    await product_service.delete_product(uow, product_response.id)
    with pytest.raises(HTTPException) as http_exc:
        await product_service.get_product(uow, product_response.id)
    assert http_exc.value.status_code == 404

