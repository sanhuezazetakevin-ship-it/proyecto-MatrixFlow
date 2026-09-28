from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey(
            "empresas.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    codigo: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    direccion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ciudad: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    telefono: Mapped[str | None] = mapped_column(
        String(30),
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

    empresa = relationship(
        "Empresa",
        back_populates="sucursales",
    )
    inventarios = relationship(
        "Inventario",
        back_populates="sucursal",
    )
    ventas = relationship(
        "Venta",
        back_populates="sucursal",
    )
    metas = relationship(
        "Meta",
        back_populates="sucursal",
    )