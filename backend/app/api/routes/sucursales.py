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

from app.schemas.sucursal_schema import (
    SucursalCreate,
    SucursalResponse,
    SucursalUpdate,
)

from app.services.sucursal_service import (
    sucursal_service,
)


router = APIRouter(
    prefix="/api/sucursales",
    tags=["Sucursales"],
)


@router.post(
    "/",
    response_model=SucursalResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_sucursal(
    data: SucursalCreate,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return sucursal_service.create(
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
            detail="No se pudo crear la sucursal.",
        )


@router.get(
    "/",
    response_model=list[SucursalResponse],
)
def listar_sucursales(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return sucursal_service.get_all(db)


@router.get(
    "/empresa/{empresa_id}",
    response_model=list[SucursalResponse],
)
def listar_sucursales_empresa(
    empresa_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return sucursal_service.get_by_empresa(
            empresa_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/{sucursal_id}",
    response_model=SucursalResponse,
)
def obtener_sucursal(
    sucursal_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return sucursal_service.get_by_id(
            sucursal_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{sucursal_id}",
    response_model=SucursalResponse,
)
def actualizar_sucursal(
    sucursal_id: int,
    data: SucursalUpdate,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return sucursal_service.update(
            sucursal_id,
            data,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la sucursal.",
        )