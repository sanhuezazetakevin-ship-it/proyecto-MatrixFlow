from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Inventario(Base):
    __tablename__ = "inventario"

    __table_args__ = (
        UniqueConstraint(
            "sucursal_id",
            "producto_id",
            name="uq_inventario_sucursal_producto",
        ),
    )

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

    producto_id: Mapped[int] = mapped_column(
        ForeignKey(
            "productos.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    stock_actual: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    stock_minimo: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    sucursal = relationship(
        "Sucursal",
        back_populates="inventarios",
    )

    producto = relationship(
        "Producto",
        back_populates="inventarios",
    )

    movimientos = relationship(
        "MovimientoInventario",
        back_populates="inventario",
    )