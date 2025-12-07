from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.submodel_schemas import Submodel, SubmodelCreate
from app.services import submodel_service
from app.exceptions.submodel_exc import (
    SubmodelAlreadyExists,
    CarModelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/submodels")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Submodel)
async def post_submodel(data: SubmodelCreate, db: AsyncSession = Depends(get_db)):
    try:
        submodel = await submodel_service.create_submodel(data, db)
        return submodel

    except CarModelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SubmodelAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
