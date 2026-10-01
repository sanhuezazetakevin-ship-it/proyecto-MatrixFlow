from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    require_role,
)
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


# ============================================================
# CREAR SUCURSAL
# Solo administrador
# ============================================================

@router.post(
    "/",
    response_model=SucursalResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_sucursal(
    data: SucursalCreate,
    current_user: Usuario = Depends(
        require_role("administrador")
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo crear la sucursal.",
        )


# ============================================================
# LISTAR SUCURSALES
# Todos los usuarios autenticados
# ============================================================

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


# ============================================================
# LISTAR SUCURSALES POR EMPRESA
# Todos los usuarios autenticados
# ============================================================

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# OBTENER SUCURSAL
# Todos los usuarios autenticados
# ============================================================

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR SUCURSAL
# Solo administrador
# ============================================================

@router.patch(
    "/{sucursal_id}",
    response_model=SucursalResponse,
)
def actualizar_sucursal(
    sucursal_id: int,
    data: SucursalUpdate,
    current_user: Usuario = Depends(
        require_role("administrador")
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar la sucursal.",
        )