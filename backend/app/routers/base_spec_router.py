from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.base_spec_schemas import (
    BaseSpecification,
    BaseSpecificationCreate,
)
from app.services import base_spec_service
from app.exceptions.base_spec_exc import (
    BaseSpecificationAlreadyExists,
    GenerationNotFound,
)
from app.exceptions.common import DatabaseIntegrityError


router = APIRouter(prefix="/base-specifications")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseSpecification)
async def post_base_specification(
    data: BaseSpecificationCreate, db: AsyncSession = Depends(get_db)
):
    try:
        base_spec = await base_spec_service.create_base_specification(data, db)
        return base_spec

    except GenerationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except BaseSpecificationAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
