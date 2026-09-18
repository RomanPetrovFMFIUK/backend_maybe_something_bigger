__all__ = (
    'ProductService',
    'UserService',
    'CatalogueService',
    'TelegramService'
)

from backend.app.services.product import ProductService
from backend.app.services.user import UserService
from backend.app.services.catalogue import CatalogueService
from backend.app.services.telegram import TelegramService