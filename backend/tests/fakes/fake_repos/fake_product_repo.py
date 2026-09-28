from backend.app.models import Product

import uuid


class FakeProductRepository:
    def __init__(self, initial_products: list[Product] | None = None):
        self._storage: dict[str, Product] = {}
        if initial_products:
            for product in initial_products:
                if not product.id:
                    product.id = str(uuid.uuid4())
                self._storage[str(product.id)] = product

    async def get_all(self) -> list[Product]:
        return list(self._storage.values())

    async def get_by_id(self, product_id: str) -> Product | None:
        return self._storage.get(product_id)

    async def create(self,
                     name: str,
                     price: int,
                     amount: int,
                     user_id: str) -> Product:

        new_product = Product(name=name,
                              price=price,
                              amount=amount,
                              user_id=user_id)

        if getattr(new_product, 'id', None) is None:
            new_product.id = str(uuid.uuid4())

        self._storage[new_product.id] = new_product
        return new_product

    async def delete(self, product: Product) -> None:
        self._storage.pop(product.id)