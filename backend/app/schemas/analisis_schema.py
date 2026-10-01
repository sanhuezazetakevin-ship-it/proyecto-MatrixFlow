from datetime import date

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class GenerarVectorEmpresaRequest(BaseModel):
    empresa_id: int = Field(gt=0)


class CompararVentasMetasRequest(BaseModel):
    vector_ventas_id: int = Field(gt=0)
    vector_metas_id: int = Field(gt=0)

class AnalisisPeriodoRequest(BaseModel):
    empresa_id: int = Field(gt=0)
    fecha_inicio: date
    fecha_fin: date

    @model_validator(mode="after")
    def validar_periodo(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser menor "
                "que la fecha inicial."
            )

        return self