from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ProductoCreate(BaseModel):
    empresa_id: int = Field(gt=0)
    categoria_id: int = Field(gt=0)

    codigo: str = Field(
        min_length=2,
        max_length=50,
    )

    nombre: str = Field(
        min_length=2,
        max_length=200,
    )

    descripcion: str | None = None

    precio: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    costo: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    unidad_medida: str = Field(
        default="unidad",
        min_length=1,
        max_length=30,
    )


class ProductoUpdate(BaseModel):
    categoria_id: int | None = Field(
        default=None,
        gt=0,
    )

    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    descripcion: str | None = None

    precio: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    costo: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    unidad_medida: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    activo: bool | None = None


class ProductoResponse(BaseModel):
    id: int
    empresa_id: int
    categoria_id: int
    codigo: str
    nombre: str
    descripcion: str | None
    precio: Decimal
    costo: Decimal
    unidad_medida: str
    activo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )