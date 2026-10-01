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

from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)

from app.services.categoria_service import (
    categoria_service,
)


router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorias"],
)


# ============================================================
# CREAR CATEGORÍA
# Solo administrador
# ============================================================

@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_categoria(
    data: CategoriaCreate,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return categoria_service.create(
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
            detail="No se pudo crear la categoría.",
        )


# ============================================================
# LISTAR CATEGORÍAS
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[CategoriaResponse],
)
def listar_categorias(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return categoria_service.get_all(db)


# ============================================================
# OBTENER CATEGORÍA
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def obtener_categoria(
    categoria_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return categoria_service.get_by_id(
            categoria_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR CATEGORÍA
# Solo administrador
# ============================================================

@router.patch(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def actualizar_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return categoria_service.update(
            categoria_id,
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
            detail="No se pudo actualizar la categoría.",
        )