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

from app.schemas.producto_schema import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
)

from app.services.producto_service import (
    producto_service,
)


router = APIRouter(
    prefix="/api/productos",
    tags=["Productos"],
)


# ============================================================
# CREAR PRODUCTO
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_producto(
    data: ProductoCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.create(
            data=data,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception as error:
        print(
            "ERROR REAL CREANDO PRODUCTO:",
            repr(error),
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"{type(error).__name__}: "
                f"{str(error)}"
            ),
        )


# ============================================================
# LISTAR PRODUCTOS
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[ProductoResponse],
)
def listar_productos(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return producto_service.get_all(db)


# ============================================================
# LISTAR PRODUCTOS POR EMPRESA
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/empresa/{empresa_id}",
    response_model=list[ProductoResponse],
)
def listar_productos_empresa(
    empresa_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.get_by_empresa(
            empresa_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# LISTAR PRODUCTOS POR CATEGORÍA
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/categoria/{categoria_id}",
    response_model=list[ProductoResponse],
)
def listar_productos_categoria(
    categoria_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.get_by_categoria(
            categoria_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# OBTENER PRODUCTO
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
)
def obtener_producto(
    producto_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.get_by_id(
            producto_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR PRODUCTO
# operador / administrador
# ============================================================

@router.patch(
    "/{producto_id}",
    response_model=ProductoResponse,
)
def actualizar_producto(
    producto_id: int,
    data: ProductoUpdate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.update(
            producto_id=producto_id,
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
        detail="No se pudo actualizar el producto.",
    )