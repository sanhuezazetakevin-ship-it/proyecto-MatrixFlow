from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
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


class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    inventario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventario.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    cantidad: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    stock_anterior: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    stock_nuevo: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    motivo: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    inventario = relationship(
        "Inventario",
        back_populates="movimientos",
    )