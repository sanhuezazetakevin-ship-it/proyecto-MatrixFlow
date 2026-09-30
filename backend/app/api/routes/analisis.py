from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from app.core.security import require_role
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.usuario_model import Usuario

from app.schemas.analisis_schema import (
    GenerarVectorEmpresaRequest,
    CompararVentasMetasRequest,
    AnalisisPeriodoRequest,
)
from app.schemas.vector_schema import (
    VectorResponse,
)

from app.services.analisis_service import (
    analisis_service,
)


router = APIRouter(
    prefix="/api/analisis",
    tags=["Análisis empresarial"],
)


# =====================================================
# VECTOR DE VENTAS POR SUCURSAL
# =====================================================

@router.post(
    "/vector-ventas",
    response_model=VectorResponse,
)
def generar_vector_ventas(
    data: GenerarVectorEmpresaRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return analisis_service.generar_vector_ventas(
            empresa_id=data.empresa_id,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# =====================================================
# VECTOR DE METAS POR SUCURSAL
# =====================================================

@router.post(
    "/vector-metas",
    response_model=VectorResponse,
)
def generar_vector_metas(
    data: GenerarVectorEmpresaRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return analisis_service.generar_vector_metas(
            empresa_id=data.empresa_id,
            usuario_id=current_user.id,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
# =====================================================
# COMPARACIÓN VENTAS VS METAS
# =====================================================

@router.post(
    "/comparar-ventas-metas",
)
def comparar_ventas_metas(
    data: CompararVentasMetasRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        operacion = (
            analisis_service.comparar_ventas_metas(
                vector_ventas_id=data.vector_ventas_id,
                vector_metas_id=data.vector_metas_id,
                usuario_id=current_user.id,
                db=db,
            )
        )

        return operacion

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
# =====================================================
# ANÁLISIS AUTOMÁTICO POR PERÍODO
# =====================================================

@router.post(
    "/ventas-vs-metas-periodo",
)
def analizar_ventas_metas_periodo(
    data: AnalisisPeriodoRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return (
            analisis_service
            .analizar_ventas_metas_periodo(
                empresa_id=data.empresa_id,
                fecha_inicio=data.fecha_inicio,
                fecha_fin=data.fecha_fin,
                usuario_id=current_user.id,
                db=db,
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )