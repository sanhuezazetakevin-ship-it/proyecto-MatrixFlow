from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey(
            "sucursales.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    numero_venta: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    impuesto: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="COMPLETADA",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    sucursal = relationship(
        "Sucursal",
        back_populates="ventas",
    )

    detalles = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan",
    )