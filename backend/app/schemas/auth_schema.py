from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class RegisterRequest(BaseModel):
    dni: str = Field(
        min_length=8,
        max_length=8,
        pattern=r"^\d{8}$"
    )
    nombre: str = Field(
        min_length=2,
        max_length=100
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=72
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    success: bool
    mensaje: str
    usuario: UserResponse

class FacialRegisterRequest(BaseModel):
    dni: str = Field(
        min_length=8,
        max_length=8
    )
    nombre: str
    email: EmailStr
    password: str