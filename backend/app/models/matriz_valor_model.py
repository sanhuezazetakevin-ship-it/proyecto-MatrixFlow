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


class MatrizValor(Base):
    __tablename__ = "matriz_valores"

    __table_args__ = (
        UniqueConstraint(
            "matriz_id",
            "fila",
            "columna",
            name="uq_matriz_fila_columna",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    matriz_id: Mapped[int] = mapped_column(
        ForeignKey(
            "matrices.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    fila: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    columna: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    matriz = relationship(
        "Matriz",
        back_populates="valores",
    )