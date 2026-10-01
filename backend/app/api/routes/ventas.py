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

from app.schemas.venta_schema import (
    VentaCreate,
    VentaResponse,
)

from app.services.venta_service import (
    venta_service,
)


router = APIRouter(
    prefix="/api/ventas",
    tags=["Ventas"],
)


# ============================================================
# CREAR VENTA
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_venta(
    data: VentaCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return venta_service.create(
            data=data,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo registrar la venta.",
        )


# ============================================================
# LISTAR VENTAS
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[VentaResponse],
)
def listar_ventas(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return venta_service.get_all(db)


# ============================================================
# LISTAR VENTAS POR SUCURSAL
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/sucursal/{sucursal_id}",
    response_model=list[VentaResponse],
)
def listar_ventas_sucursal(
    sucursal_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return venta_service.get_by_sucursal(
            sucursal_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# LISTAR VENTAS COMPLETADAS
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/completadas",
    response_model=list[VentaResponse],
)
def listar_ventas_completadas(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return venta_service.get_completadas(db)


# ============================================================
# OBTENER VENTA
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{venta_id}",
    response_model=VentaResponse,
)
def obtener_venta(
    venta_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return venta_service.get_by_id(
            venta_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ANULAR VENTA
# operador / administrador
# ============================================================

@router.patch(
    "/{venta_id}/anular",
    response_model=VentaResponse,
)
def anular_venta(
    venta_id: int,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return venta_service.anular(
            venta_id=venta_id,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo anular la venta.",
        )