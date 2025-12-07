from fastapi import APIRouter

from app.routers import brand_router, car_model_router, submodel_router


main_router = APIRouter()
main_router.include_router(brand_router.router)
main_router.include_router(car_model_router.router)
main_router.include_router(submodel_router.router)
