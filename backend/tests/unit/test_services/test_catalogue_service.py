from backend.app.schemas import (
    CatalogueCreate,
    ProductCreate)


async def test_add_product_to_catalogue(uow, catalogue_service, product_service):
    catalogue_create_schema = CatalogueCreate(name="test_catalogue")

    product_create_schema = ProductCreate(
        name="test_product",
        price=100,
        amount=100,
        user_id="test_id_user"
    )

    new_catalogue = await catalogue_service.create_catalogue(
        uow, catalogue_create_schema
    )
    product = await product_service.create_product(uow, product_create_schema)

    await catalogue_service.add_product_to_catalogue(
        uow,
        product,
        new_catalogue
    )
    result = await catalogue_service.list_products_by_catalogue_id(
        uow,
        new_catalogue.id,
        15,
        0
    )
    assert product
    assert product in result


async def test_delete_product_from_catalogue(uow, catalogue_service, product_service):
    catalogue_create_schema = CatalogueCreate(name="test_catalogue")

    product_create_schema = ProductCreate(
        name="test_product",
        price=100,
        amount=100,
        user_id="test_id_user"
    )

    new_catalogue = await catalogue_service.create_catalogue(
        uow, catalogue_create_schema
    )
    product = await product_service.create_product(uow, product_create_schema)

    await catalogue_service.add_product_to_catalogue(
        uow,
        product,
        new_catalogue
    )

    await catalogue_service.delete_product_from_catalogue(uow, product, new_catalogue)

    result = await catalogue_service.list_products_by_catalogue_id(
        uow,
        new_catalogue.id,
        15,
        0
    )

    assert result == []


async def test_list_products(uow, catalogue_service, product_service):
    catalogue_create_schema = CatalogueCreate(name="test_catalogue")

    product_create_schema1 = ProductCreate(
        name="test_product1",
        price=100,
        amount=100,
        user_id="test_id_user"
    )

    product_create_schema2 = ProductCreate(
        name="test_product2",
        price=100,
        amount=100,
        user_id="test_id_user"
    )

    new_catalogue = await catalogue_service.create_catalogue(
        uow, catalogue_create_schema
    )
    product1 = await product_service.create_product(uow, product_create_schema1)

    product2 = await product_service.create_product(uow, product_create_schema2)


    await catalogue_service.add_product_to_catalogue(
        uow,
        product1,
        new_catalogue
    )

    await catalogue_service.add_product_to_catalogue(
        uow,
        product2,
        new_catalogue
    )

    result_without_offset = await catalogue_service.list_products_by_catalogue_id(
        uow,
        new_catalogue.id,
        2,
        0
    )

    result_with_1_offset = await catalogue_service.list_products_by_catalogue_id(
        uow,
        new_catalogue.id,
        2,
        1
    )

    assert len(result_with_1_offset) == 1
    assert len(result_without_offset) == 2

