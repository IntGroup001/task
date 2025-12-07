from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.generation_schemas import Generation, GenerationCreate
from app.services import generation_service
from app.exceptions.generation_exc import (
    GenerationAlreadyExists,
    SubmodelNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/generations")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Generation)
async def post_generation(data: GenerationCreate, db: AsyncSession = Depends(get_db)):
    try:
        generation = await generation_service.create_generation(data, db)
        return generation

    except SubmodelNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except GenerationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
