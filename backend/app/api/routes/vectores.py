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

from app.schemas.vector_schema import (
    VectorCreate,
    VectorResponse,
    VectorUpdate,
)

from app.services.vector_service import (
    vector_service,
)


router = APIRouter(
    prefix="/api/vectores",
    tags=["Vectores"],
)


# ============================================================
# CREAR VECTOR
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=VectorResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_vector(
    data: VectorCreate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return vector_service.create(
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
            detail="No se pudo crear el vector.",
        )


# ============================================================
# LISTAR VECTORES
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/",
    response_model=list[VectorResponse],
)
def listar_vectores(
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return vector_service.get_all(db)


# ============================================================
# OBTENER VECTOR
# Todos los usuarios autenticados
# ============================================================

@router.get(
    "/{vector_id}",
    response_model=VectorResponse,
)
def obtener_vector(
    vector_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return vector_service.get_by_id(
            vector_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# ============================================================
# ACTUALIZAR VECTOR
# operador / administrador
# ============================================================

@router.patch(
    "/{vector_id}",
    response_model=VectorResponse,
)
def actualizar_vector(
    vector_id: int,
    data: VectorUpdate,
    current_user: Usuario = Depends(
        require_role("operador", "administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return vector_service.update(
            vector_id,
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
            detail="No se pudo actualizar el vector.",
        )


# ============================================================
# ELIMINAR VECTOR
# Solo administrador
# ============================================================

@router.delete(
    "/{vector_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_vector(
    vector_id: int,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        vector_service.delete(
            vector_id,
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
            detail="No se pudo eliminar el vector.",
        )