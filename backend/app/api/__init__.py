from fastapi import APIRouter

from backend.app.api.users import router as user_router
from backend.app.api.products import router as product_router
from backend.app.api.catalogues import router as catalogues_router

router = APIRouter()
router.include_router(user_router)
router.include_router(product_router)
router.include_router(catalogues_router)
