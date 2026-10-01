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

from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaResponse,
    EmpresaUpdate,
)

from app.services.empresa_service import (
    empresa_service,
)


router = APIRouter(
    prefix="/api/empresas",
    tags=["Empresas"],
)


@router.post(
    "/",
    response_model=EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_empresa(
    data: EmpresaCreate,
    current_user: Usuario = Depends(
    require_role("administrador")
),
    db: Session = Depends(get_db),
):
    try:
        return empresa_service.create(
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
            detail="No se pudo crear la empresa.",
        )


@router.get(
    "/",
    response_model=list[EmpresaResponse],
)
def listar_empresas(
    current_user: Usuario = Depends(
            get_current_user
        ),
    db: Session = Depends(get_db),
):
    return empresa_service.get_all(db)


@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse,
)
def obtener_empresa(
    empresa_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    try:
        return empresa_service.get_by_id(
            empresa_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )


@router.patch(
    "/{empresa_id}",
    response_model=EmpresaResponse,
)
def actualizar_empresa(
    empresa_id: int,
    data: EmpresaUpdate,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return empresa_service.update(
            empresa_id,
            data,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la empresa.",
        )