from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class MatrizCreate(BaseModel):
    nombre: str = Field(
        min_length=1,
        max_length=150,
    )

    descripcion: str | None = None

    valores: list[list[Decimal]] = Field(
        min_length=1,
    )

    @model_validator(mode="after")
    def validar_matriz(self):

        if not self.valores:
            raise ValueError(
                "La matriz debe contener filas."
            )

        columnas = len(self.valores[0])

        if columnas == 0:
            raise ValueError(
                "La matriz debe contener columnas."
            )

        for fila in self.valores:

            if len(fila) != columnas:
                raise ValueError(
                    "Todas las filas deben tener "
                    "la misma cantidad de columnas."
                )

        return self


class MatrizUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    descripcion: str | None = None


class MatrizValorResponse(BaseModel):
    fila: int
    columna: int
    valor: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class MatrizResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None

    filas: int
    columnas: int

    usuario_id: int
    created_at: datetime

    valores: list[MatrizValorResponse]

    model_config = ConfigDict(
        from_attributes=True
    )