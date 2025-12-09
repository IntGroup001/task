from fastapi import APIRouter

from app.routers import (
    brand_router,
    car_model_router,
    submodel_router,
    generation_router,
    base_spec_router,
    car_data_router,
    user_router,
    auth_router,
)


main_router = APIRouter()
main_router.include_router(brand_router.router)
main_router.include_router(car_model_router.router)
main_router.include_router(submodel_router.router)
main_router.include_router(generation_router.router)
main_router.include_router(base_spec_router.router)
main_router.include_router(car_data_router.router)
main_router.include_router(user_router.router)
main_router.include_router(auth_router.router)
