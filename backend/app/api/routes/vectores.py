from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy.orm import Session
from app.core.security import require_role
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


@router.post(
    "/",
    response_model=VectorResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_vector(
    data: VectorCreate,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
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
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el vector.",
        )


@router.get(
    "/",
    response_model=list[VectorResponse],
)
def listar_vectores(
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    return vector_service.get_all(db)


@router.get(
    "/{vector_id}",
    response_model=VectorResponse,
)
def obtener_vector(
    vector_id: int,
    current_user: Usuario = Depends(
       require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:
        return vector_service.get_by_id(
            vector_id,
            db,
            usuario_id=current_user.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{vector_id}",
    response_model=VectorResponse,
)
def actualizar_vector(
    vector_id: int,
    data: VectorUpdate,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return vector_service.update(
            vector_id,
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
            detail="No se pudo actualizar el vector.",
        )


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
            usuario_id=current_user.id,
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar el vector.",
        )