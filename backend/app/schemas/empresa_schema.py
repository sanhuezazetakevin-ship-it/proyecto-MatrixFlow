from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class EmpresaCreate(BaseModel):
    ruc: str = Field(
        min_length=11,
        max_length=11,
        pattern=r"^\d{11}$",
    )

    razon_social: str = Field(
        min_length=2,
        max_length=200,
    )

    nombre_comercial: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None


class EmpresaUpdate(BaseModel):
    razon_social: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )
    nombre_comercial: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
    activo: bool | None = None


class EmpresaResponse(BaseModel):
    id: int
    ruc: str
    razon_social: str
    nombre_comercial: str | None
    direccion: str | None
    telefono: str | None
    email: str | None
    activo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )