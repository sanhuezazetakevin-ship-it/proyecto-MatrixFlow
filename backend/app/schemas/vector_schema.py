from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class VectorCreate(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=150,
    )

    descripcion: str | None = None

    valores: list[Decimal] = Field(
        min_length=1,
        max_length=1000,
    )


class VectorUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    descripcion: str | None = None


class VectorValorResponse(BaseModel):
    posicion: int
    valor: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class VectorResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    dimension: int
    usuario_id: int
    created_at: datetime

    valores: list[VectorValorResponse]

    model_config = ConfigDict(
        from_attributes=True
    )