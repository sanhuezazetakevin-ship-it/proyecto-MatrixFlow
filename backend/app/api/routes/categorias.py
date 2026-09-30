from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
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

from app.core.security import require_role

require_role("administrador")


router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorias"],
)


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_categoria(
    data: CategoriaCreate,
    current_user: Usuario = Depends(
    require_role(
        "administrador"
    )
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
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear la categoría.",
        )


@router.get(
    "/",
    response_model=list[CategoriaResponse],
)
def listar_categorias(
    current_user: Usuario = Depends(
        require_role(
        "administrador",
        "analista",
        "consulta" 
    )
    ),
    db: Session = Depends(get_db),
):
    return categoria_service.get_all(db)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def obtener_categoria(
    categoria_id: int,
    current_user: Usuario = Depends(
        require_role(
        "administrador",
        "analista",
        "consulta"
    )
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
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{categoria_id}",
    response_model=CategoriaResponse,
)
def actualizar_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    current_user: Usuario = Depends(
        require_role(
        "administrador"
    )
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
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la categoría.",
        )