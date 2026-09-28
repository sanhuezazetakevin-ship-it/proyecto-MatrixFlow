from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class InventarioCreate(BaseModel):
    sucursal_id: int = Field(gt=0)
    producto_id: int = Field(gt=0)

    stock_inicial: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )

    stock_minimo: Decimal = Field(
        default=Decimal("0"),
        ge=0,
    )


class InventarioUpdate(BaseModel):
    stock_minimo: Decimal = Field(
        ge=0,
    )


class InventarioResponse(BaseModel):
    id: int
    sucursal_id: int
    producto_id: int
    stock_actual: Decimal
    stock_minimo: Decimal
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class MovimientoCreate(BaseModel):
    tipo: str
    cantidad: Decimal = Field(gt=0)
    motivo: str | None = None


class MovimientoResponse(BaseModel):
    id: int
    inventario_id: int
    tipo: str
    cantidad: Decimal
    stock_anterior: Decimal
    stock_nuevo: Decimal
    motivo: str | None
    usuario_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )