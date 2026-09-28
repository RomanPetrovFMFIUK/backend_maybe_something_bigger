import pytest
from backend.tests.fakes.fake_repos import FakeUnitOfWork
from backend.app.services import UserService, ProductService, CatalogueService

@pytest.fixture
def uow():
    return FakeUnitOfWork()

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def product_service():
    return ProductService()

@pytest.fixture
def catalogue_service():
    return CatalogueService()