from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    venta_id: Mapped[int] = mapped_column(
        ForeignKey(
            "ventas.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey(
            "productos.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    cantidad: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    venta = relationship(
        "Venta",
        back_populates="detalles",
    )

    producto = relationship(
        "Producto",
    )