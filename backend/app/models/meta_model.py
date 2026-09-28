from datetime import (
    date,
    datetime,
)
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Meta(Base):
    __tablename__ = "metas"

    __table_args__ = (
        UniqueConstraint(
            "sucursal_id",
            "tipo",
            "fecha_inicio",
            "fecha_fin",
            name="uq_meta_sucursal_tipo_periodo",
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

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="VENTAS",
        index=True,
    )

    valor_objetivo: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    sucursal = relationship(
        "Sucursal",
        back_populates="metas",
    )