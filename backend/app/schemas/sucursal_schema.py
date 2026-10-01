from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class SucursalCreate(BaseModel):
    empresa_id: int = Field(
        gt=0
    )

    nombre: str = Field(
        min_length=2,
        max_length=150,
    )

    codigo: str = Field(
        min_length=2,
        max_length=30,
    )

    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None


class SucursalUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None
    activo: bool | None = None


class SucursalResponse(BaseModel):
    id: int
    empresa_id: int
    nombre: str
    codigo: str
    direccion: str | None
    ciudad: str | None
    telefono: str | None
    activo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )