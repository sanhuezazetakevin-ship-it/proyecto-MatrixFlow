from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# =====================================================
# REQUESTS
# =====================================================


class OperacionDosVectoresRequest(BaseModel):
    vector_a_id: int = Field(gt=0)
    vector_b_id: int = Field(gt=0)


class OperacionVectorEscalarRequest(BaseModel):
    vector_id: int = Field(gt=0)
    escalar: float


class OperacionDosMatricesRequest(BaseModel):
    matriz_a_id: int = Field(gt=0)
    matriz_b_id: int = Field(gt=0)


class OperacionMatrizRequest(BaseModel):
    matriz_id: int = Field(gt=0)


class OperacionMatrizEscalarRequest(BaseModel):
    matriz_id: int = Field(gt=0)
    escalar: float


class CombinacionLinealRequest(BaseModel):
    vector_ids: list[int] = Field(
        min_length=1,
    )

    coeficientes: list[float] = Field(
        min_length=1,
    )


# =====================================================
# RESPONSES
# =====================================================


class OperacionEntradaResponse(BaseModel):
    id: int
    tipo_objeto: str
    referencia_id: int | None
    nombre: str | None
    orden: int

    datos: (
        dict
        | list
        | float
        | int
    )

    model_config = ConfigDict(
        from_attributes=True
    )


class OperacionResultadoResponse(BaseModel):
    id: int
    tipo_resultado: str

    datos: (
        dict
        | list
        | float
        | int
    )

    model_config = ConfigDict(
        from_attributes=True
    )


class OperacionResponse(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    estado: str
    mensaje_error: str | None
    created_at: datetime

    entradas: list[
        OperacionEntradaResponse
    ]

    resultado: (
        OperacionResultadoResponse
        | None
    )

    model_config = ConfigDict(
        from_attributes=True
    )