from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.connection import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    ruc: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False,
        index=True,
    )

    razon_social: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    nombre_comercial: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    direccion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    sucursales = relationship(
        "Sucursal",
        back_populates="empresa",
    )
    productos = relationship(
        "Producto",
        back_populates="empresa",
    )