from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class PersonaCreate(BaseModel):

    dni: str = Field(
        min_length=8,
        max_length=8
    )

    nombre: str

    email: EmailStr


class PersonaResponse(BaseModel):

    id: int
    dni: str
    nombre: str
    email: str
    activo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )