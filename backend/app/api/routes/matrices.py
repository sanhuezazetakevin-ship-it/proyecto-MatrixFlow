from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    require_role,
)
from app.database.connection import get_db
from app.models.usuario_model import Usuario

from app.schemas.matriz_schema import (
    MatrizCreate,
    MatrizResponse,
    MatrizUpdate,
)

from app.services.matriz_service import (
    matriz_service,
)


router = APIRouter(
    prefix="/api/matrices",
    tags=["Matrices"],
)


# ============================================================
# CREAR MATRIZ
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=MatrizResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_matriz(
    data: MatrizCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return matriz_service.create(
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
            detail="No se pudo crear la matriz.",
        )


# ============================================================
# LISTAR MATRICES
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[MatrizResponse],
)
def listar_matrices(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return matriz_service.get_all(db)


# ============================================================
# OBTENER MATRIZ
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{matriz_id}",
    response_model=MatrizResponse,
)
def obtener_matriz(
    matriz_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return matriz_service.get_by_id(
            matriz_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR MATRIZ
# operador / administrador
# ============================================================

@router.patch(
    "/{matriz_id}",
    response_model=MatrizResponse,
)
def actualizar_matriz(
    matriz_id: int,
    data: MatrizUpdate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return matriz_service.update(
            matriz_id,
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
            detail="No se pudo actualizar la matriz.",
        )


# ============================================================
# ELIMINAR MATRIZ
# Solo administrador
# ============================================================

@router.delete(
    "/{matriz_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_matriz(
    matriz_id: int,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        matriz_service.delete(
            matriz_id,
            db,
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo eliminar la matriz.",
        )