from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DetalleVentaCreate(BaseModel):
    producto_id: int = Field(gt=0)

    cantidad: Decimal = Field(
        gt=0,
        max_digits=14,
        decimal_places=2,
    )


class VentaCreate(BaseModel):
    sucursal_id: int = Field(gt=0)

    productos: list[DetalleVentaCreate] = Field(
        min_length=1,
    )


class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: Decimal
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class VentaResponse(BaseModel):
    id: int
    sucursal_id: int
    usuario_id: int
    numero_venta: str
    subtotal: Decimal
    impuesto: Decimal
    total: Decimal
    estado: str
    created_at: datetime

    detalles: list[DetalleVentaResponse]

    model_config = ConfigDict(
        from_attributes=True
    )