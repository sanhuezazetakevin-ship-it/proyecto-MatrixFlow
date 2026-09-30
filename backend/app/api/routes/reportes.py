from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session
from datetime import date
from app.core.security import require_role

from app.database.connection import (
    get_db,
)

from app.models.usuario_model import (
    Usuario,
)

from app.schemas.reporte_schema import (
    DashboardResponse,
    IndicadoresPeriodoResponse,
    VentasProductosResponse,
    EstadoInventarioResponse,
)

from app.services.reporte_service import (
    reporte_service,
)


router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes"],
)


# =====================================================
# DASHBOARD EMPRESARIAL
# =====================================================

@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
def obtener_dashboard(
    empresa_id: int = Query(
        ...,
        gt=0,
    ),
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:

        return (
            reporte_service
            .obtener_dashboard(
                empresa_id=empresa_id,
                db=db,
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
# =====================================================
# INDICADORES POR PERÍODO
# =====================================================

@router.get(
    "/indicadores-periodo",
    response_model=IndicadoresPeriodoResponse,
)
def obtener_indicadores_periodo(
    empresa_id: int = Query(
        ...,
        gt=0,
    ),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:

        return (
            reporte_service
            .obtener_indicadores_periodo(
                empresa_id=empresa_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                db=db,
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

# =====================================================
# VENTAS POR PRODUCTO
# =====================================================

@router.get(
    "/ventas-productos",
    response_model=VentasProductosResponse,
)
def obtener_ventas_productos(
    empresa_id: int = Query(..., gt=0),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:
        return reporte_service.obtener_ventas_productos(
            empresa_id=empresa_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            db=db,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# =====================================================
# ESTADO DEL INVENTARIO
# =====================================================

@router.get(
    "/inventario",
    response_model=EstadoInventarioResponse,
)
def obtener_estado_inventario(
    empresa_id: int = Query(..., gt=0),
    current_user: Usuario = Depends(
        require_role("administrador", "analista", "consulta")
    ),
    db: Session = Depends(get_db),
):
    try:
        return (
            reporte_service
            .obtener_estado_inventario(
                empresa_id=empresa_id,
                db=db,
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )