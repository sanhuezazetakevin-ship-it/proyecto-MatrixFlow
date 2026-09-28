from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CategoriaCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
    )

    descripcion: str | None = None


class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    descripcion: str | None = None
    activo: bool | None = None


class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )