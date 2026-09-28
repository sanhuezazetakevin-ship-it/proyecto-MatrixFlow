from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Producto(Base):
    __tablename__ = "productos"

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

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categorias.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    precio: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    costo: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    unidad_medida: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="unidad",
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
        back_populates="productos",
    )

    categoria = relationship(
        "Categoria",
        back_populates="productos",
    )
    inventarios = relationship(
        "Inventario",
        back_populates="producto",
    )