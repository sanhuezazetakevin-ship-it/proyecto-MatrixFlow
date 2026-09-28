from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.usuario_model import Usuario

from app.schemas.meta_schema import (
    CumplimientoMetaResponse,
    MetaCreate,
    MetaResponse,
    MetaUpdate,
)

from app.services.meta_service import (
    meta_service,
)


router = APIRouter(
    prefix="/api/metas",
    tags=["Metas"],
)


@router.post(
    "/",
    response_model=MetaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_meta(
    data: MetaCreate,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return meta_service.create(
            data,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear la meta.",
        )


@router.get(
    "/",
    response_model=list[MetaResponse],
)
def listar_metas(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return meta_service.get_all(db)


@router.get(
    "/sucursal/{sucursal_id}",
    response_model=list[MetaResponse],
)
def listar_metas_sucursal(
    sucursal_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return meta_service.get_by_sucursal(
            sucursal_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/{meta_id}/cumplimiento",
    response_model=CumplimientoMetaResponse,
)
def obtener_cumplimiento(
    meta_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return meta_service.cumplimiento(
            meta_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/{meta_id}",
    response_model=MetaResponse,
)
def obtener_meta(
    meta_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return meta_service.get_by_id(
            meta_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{meta_id}",
    response_model=MetaResponse,
)
def actualizar_meta(
    meta_id: int,
    data: MetaUpdate,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return meta_service.update(
            meta_id,
            data,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la meta.",
        )