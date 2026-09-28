from decimal import Decimal
from datetime import date


from pydantic import (
    BaseModel,
    ConfigDict,
)


class ResumenDashboard(BaseModel):
    total_sucursales: int
    total_productos: int
    cantidad_ventas: int
    ventas_completadas: Decimal
    stock_total: Decimal
    productos_stock_bajo: int


class VentaSucursalDashboard(BaseModel):
    sucursal_id: int
    sucursal: str
    total_ventas: Decimal


class DashboardResponse(BaseModel):
    empresa_id: int
    resumen: ResumenDashboard
    ventas_por_sucursal: list[
        VentaSucursalDashboard
    ]

    model_config = ConfigDict(
        from_attributes=True
    )
class IndicadorSucursalResponse(BaseModel):
    sucursal_id: int
    sucursal: str
    ventas: Decimal
    meta: Decimal
    diferencia: Decimal
    porcentaje_cumplimiento: float


class IndicadoresPeriodoResponse(BaseModel):
    empresa_id: int
    fecha_inicio: date
    fecha_fin: date

    total_ventas: Decimal
    total_metas: Decimal
    diferencia_total: Decimal
    porcentaje_cumplimiento: float

    sucursales: list[
        IndicadorSucursalResponse
    ]
class VentaProductoResponse(BaseModel):
    producto_id: int
    producto: str
    cantidad_vendida: Decimal
    total_vendido: Decimal


class VentasProductosResponse(BaseModel):
    empresa_id: int
    fecha_inicio: date
    fecha_fin: date
    productos: list[VentaProductoResponse]


class InventarioProductoResponse(BaseModel):
    inventario_id: int
    sucursal_id: int
    sucursal: str
    producto_id: int
    producto: str
    stock_actual: Decimal
    stock_minimo: Decimal
    estado: str


class EstadoInventarioResponse(BaseModel):
    empresa_id: int
    total_registros: int
    stock_bajo: int
    sin_stock: int
    productos: list[InventarioProductoResponse]