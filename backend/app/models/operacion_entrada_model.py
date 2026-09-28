from sqlalchemy import (
    ForeignKey,
    Integer,
    JSON,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class OperacionEntrada(Base):
    __tablename__ = "operation_inputs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    operacion_id: Mapped[int] = mapped_column(
        ForeignKey(
            "operaciones.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    tipo_objeto: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    referencia_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    nombre: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    orden: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    datos: Mapped[dict | list | float | int] = mapped_column(
        JSON,
        nullable=False,
    )

    operacion = relationship(
        "Operacion",
        back_populates="entradas",
    )