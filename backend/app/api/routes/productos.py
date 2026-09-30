from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.core.security import require_role
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


@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_producto(
    data: ProductoCreate,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.create(
            data,
            db,
            usuario_id=current_user.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el producto.",
        )


@router.get(
    "/",
    response_model=list[ProductoResponse],
)
def listar_productos(
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    return producto_service.get_all(db)


@router.get(
    "/empresa/{empresa_id}",
    response_model=list[ProductoResponse],
)
def listar_productos_empresa(
    empresa_id: int,
    current_user: Usuario = Depends(
       require_role("administrador", "analista", "consulta")
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
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/categoria/{categoria_id}",
    response_model=list[ProductoResponse],
)
def listar_productos_categoria(
    categoria_id: int,
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
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
            status_code=404,
            detail=str(error),
        )


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
)
def obtener_producto(
    producto_id: int,
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
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
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{producto_id}",
    response_model=ProductoResponse,
)
def actualizar_producto(
    producto_id: int,
    data: ProductoUpdate,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return producto_service.update(
            producto_id,
            data,
            db,
            usuario_id=current_user.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el producto.",
        )