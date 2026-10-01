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

from app.schemas.inventario_schema import (
    InventarioCreate,
    InventarioResponse,
    InventarioUpdate,
    MovimientoCreate,
    MovimientoResponse,
)

from app.services.inventario_service import (
    inventario_service,
)


router = APIRouter(
    prefix="/api/inventario",
    tags=["Inventario"],
)


# ============================================================
# CREAR INVENTARIO
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=InventarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_inventario(
    data: InventarioCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.create(
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
            detail="No se pudo crear el inventario.",
        )


# ============================================================
# LISTAR INVENTARIO
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[InventarioResponse],
)
def listar_inventario(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return inventario_service.get_all(db)


# ============================================================
# LISTAR INVENTARIO POR SUCURSAL
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/sucursal/{sucursal_id}",
    response_model=list[InventarioResponse],
)
def listar_inventario_sucursal(
    sucursal_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.get_by_sucursal(
            sucursal_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# OBTENER INVENTARIO
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{inventario_id}",
    response_model=InventarioResponse,
)
def obtener_inventario(
    inventario_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.get_by_id(
            inventario_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR INVENTARIO
# operador / administrador
# ============================================================

@router.patch(
    "/{inventario_id}",
    response_model=InventarioResponse,
)
def actualizar_inventario(
    inventario_id: int,
    data: InventarioUpdate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.update(
            inventario_id=inventario_id,
            data=data,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el inventario.",
        )


# ============================================================
# REGISTRAR MOVIMIENTO
# operador / administrador
# ============================================================

@router.post(
    "/{inventario_id}/movimientos",
    response_model=MovimientoResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_movimiento(
    inventario_id: int,
    data: MovimientoCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.registrar_movimiento(
            inventario_id=inventario_id,
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
            detail="No se pudo registrar el movimiento.",
        )


# ============================================================
# LISTAR MOVIMIENTOS
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{inventario_id}/movimientos",
    response_model=list[MovimientoResponse],
)
def listar_movimientos(
    inventario_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return inventario_service.get_movimientos(
            inventario_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )