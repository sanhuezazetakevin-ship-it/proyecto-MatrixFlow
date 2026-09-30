from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.algorithms.linear_algebra import (
    LinearAlgebraError,
)
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.core.security import require_role
from app.schemas.operacion_schema import (
    CombinacionLinealRequest,
    OperacionDosMatricesRequest,
    OperacionDosVectoresRequest,
    OperacionMatrizEscalarRequest,
    OperacionMatrizRequest,
    OperacionResponse,
    OperacionVectorEscalarRequest,
)

from app.services.operacion_service import (
    operacion_service,
)


router = APIRouter(
    prefix="/api/operaciones",
    tags=["Operaciones matemáticas"],
)


# =====================================================
# VECTORES
# =====================================================


@router.post(
    "/vectores/suma",
    response_model=OperacionResponse,
)
def sumar_vectores(
    data: OperacionDosVectoresRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.sumar_vectores(
            data.vector_a_id,
            data.vector_b_id,
            current_user.id,
            db,
        )

    except (
        ValueError,
        LinearAlgebraError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/vectores/resta",
    response_model=OperacionResponse,
)
def restar_vectores(
    data: OperacionDosVectoresRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.restar_vectores(
            data.vector_a_id,
            data.vector_b_id,
            current_user.id,
            db,
        )

    except (
        ValueError,
        LinearAlgebraError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/vectores/escalar",
    response_model=OperacionResponse,
)
def multiplicar_vector_escalar(
    data: OperacionVectorEscalarRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.escalar_vector(
            data.vector_id,
            data.escalar,
            current_user.id,
            db,
        )

    except (
        ValueError,
        LinearAlgebraError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/vectores/producto-punto",
    response_model=OperacionResponse,
)
def producto_punto(
    data: OperacionDosVectoresRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.producto_punto(
            data.vector_a_id,
            data.vector_b_id,
            current_user.id,
            db,
        )

    except (
        ValueError,
        LinearAlgebraError,
    ) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

# =====================================================
# MATRICES
# =====================================================


@router.post(
    "/matrices/suma",
    response_model=OperacionResponse,
)
def sumar_matrices(
    data: OperacionDosMatricesRequest,
    current_user: Usuario = Depends(require_role("administrador", "analista")),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.sumar_matrices(
            data.matriz_a_id,
            data.matriz_b_id,
            current_user.id,
            db,
        )
    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/matrices/resta",
    response_model=OperacionResponse,
)
def restar_matrices(
    data: OperacionDosMatricesRequest,
    current_user: Usuario = Depends(require_role("administrador", "analista")),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.restar_matrices(
            data.matriz_a_id,
            data.matriz_b_id,
            current_user.id,
            db,
        )
    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/matrices/multiplicacion",
    response_model=OperacionResponse,
)
def multiplicar_matrices(
    data: OperacionDosMatricesRequest,
    current_user: Usuario = Depends(require_role("administrador", "analista")),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.multiplicar_matrices(
            data.matriz_a_id,
            data.matriz_b_id,
            current_user.id,
            db,
        )
    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/matrices/transpuesta",
    response_model=OperacionResponse,
)
def transponer_matriz(
    data: OperacionMatrizRequest,
    current_user: Usuario = Depends(require_role("administrador", "analista")),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.transponer_matriz(
            data.matriz_id,
            current_user.id,
            db,
        )
    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.post(
    "/matrices/escalar",
    response_model=OperacionResponse,
)
def multiplicar_matriz_escalar(
    data: OperacionMatrizEscalarRequest,
    current_user: Usuario = Depends(require_role("administrador", "analista")),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.escalar_matriz(
            data.matriz_id,
            data.escalar,
            current_user.id,
            db,
        )
    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

# =====================================================
# COMBINACIÓN LINEAL
# =====================================================


@router.post(
    "/combinacion-lineal",
    response_model=OperacionResponse,
)
def combinacion_lineal(
    data: CombinacionLinealRequest,
    current_user: Usuario = Depends(
        require_role("administrador", "analista")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.combinacion_lineal(
            data.vector_ids,
            data.coeficientes,
            current_user.id,
            db,
        )

    except (ValueError, LinearAlgebraError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
# =====================================================
# HISTORIAL
# =====================================================


@router.get(
    "/",
    response_model=list[OperacionResponse],
)
def listar_operaciones(
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    return operacion_service.get_all(db)


@router.get(
    "/{operacion_id}",
    response_model=OperacionResponse,
)
def obtener_operacion(
    operacion_id: int,
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:
        return operacion_service.get_by_id(
            operacion_id,
            db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )