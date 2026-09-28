from decimal import Decimal

from sqlalchemy import (
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


class VectorValor(Base):
    __tablename__ = "vector_valores"

    __table_args__ = (
        UniqueConstraint(
            "vector_id",
            "posicion",
            name="uq_vector_posicion",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    vector_id: Mapped[int] = mapped_column(
        ForeignKey(
            "vectores.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    posicion: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    vector = relationship(
        "Vector",
        back_populates="valores",
    )