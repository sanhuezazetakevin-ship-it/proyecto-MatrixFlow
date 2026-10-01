from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.schemas.audit_schema import AuditResponse
from app.services.audit_service import audit_service


router = APIRouter(
    prefix="/api/auditoria",
    tags=["Auditoría"],
)


# ============================================================
# LISTAR AUDITORÍA
# Solo administrador
# ============================================================

@router.get(
    "/",
    response_model=list[AuditResponse],
)
def listar_auditoria(
    limite: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    return audit_service.listar(
        db=db,
        limite=limite,
    )


# ============================================================
# AUDITORÍA POR USUARIO
# Solo administrador
# ============================================================

@router.get(
    "/usuario/{usuario_id}",
    response_model=list[AuditResponse],
)
def listar_auditoria_usuario(
    usuario_id: int,
    limite: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    return audit_service.listar_por_usuario(
        usuario_id=usuario_id,
        db=db,
        limite=limite,
    )


# ============================================================
# AUDITORÍA POR ENTIDAD
# Solo administrador
# ============================================================

@router.get(
    "/entidad/{entidad}",
    response_model=list[AuditResponse],
)
def listar_auditoria_entidad(
    entidad: str,
    limite: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    try:
        return audit_service.listar_por_entidad(
            entidad=entidad,
            db=db,
            limite=limite,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )