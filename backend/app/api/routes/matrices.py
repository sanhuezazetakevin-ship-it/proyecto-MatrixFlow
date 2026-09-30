from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.core.security import require_role
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


@router.post(
    "/",
    response_model=MatrizResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_matriz(
    data: MatrizCreate,
    current_user: Usuario = Depends(
       require_role("administrador", "analista")
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
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear la matriz.",
        )


@router.get(
    "/",
    response_model=list[MatrizResponse],
)
def listar_matrices(
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    return matriz_service.get_all(db)


@router.get(
    "/{matriz_id}",
    response_model=MatrizResponse,
)
def obtener_matriz(
    matriz_id: int,
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:
        return matriz_service.get_by_id(
            matriz_id,
            db,
            usuario_id=current_user.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{matriz_id}",
    response_model=MatrizResponse,
)
def actualizar_matriz(
    matriz_id: int,
    data: MatrizUpdate,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return matriz_service.update(
            matriz_id,
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
            detail="No se pudo actualizar la matriz.",
        )


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
            detail="No se pudo eliminar la matriz.",
        )