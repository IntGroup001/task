from fastapi import APIRouter

from app.routers import brand_router


main_router = APIRouter()
main_router.include_router(brand_router.router)
