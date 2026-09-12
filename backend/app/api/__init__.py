from fastapi import APIRouter

from .users import router as user_router
from .products import router as product_router
from .catalogues import router as catalogues_router

router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(catalogues_router)
