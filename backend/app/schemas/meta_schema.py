from datetime import (
    date,
    datetime,
)
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class MetaCreate(BaseModel):
    sucursal_id: int = Field(gt=0)

    tipo: str = Field(
        default="VENTAS",
        min_length=2,
        max_length=30,
    )

    valor_objetivo: Decimal = Field(
        gt=0,
    )

    fecha_inicio: date
    fecha_fin: date

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser "
                "anterior a la fecha inicial."
            )

        return self


class MetaUpdate(BaseModel):
    valor_objetivo: Decimal | None = Field(
        default=None,
        gt=0,
    )

    fecha_inicio: date | None = None
    fecha_fin: date | None = None


class MetaResponse(BaseModel):
    id: int
    sucursal_id: int
    tipo: str
    valor_objetivo: Decimal
    fecha_inicio: date
    fecha_fin: date
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CumplimientoMetaResponse(BaseModel):
    meta_id: int
    sucursal_id: int

    valor_objetivo: Decimal
    ventas_reales: Decimal

    diferencia: Decimal
    porcentaje_cumplimiento: Decimal

    fecha_inicio: date
    fecha_fin: date