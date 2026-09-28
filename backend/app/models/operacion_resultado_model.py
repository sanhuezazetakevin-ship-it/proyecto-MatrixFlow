from sqlalchemy import (
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class OperacionResultado(Base):
    __tablename__ = "operation_results"

    __table_args__ = (
        UniqueConstraint(
            "operacion_id",
            name="uq_resultado_operacion",
        ),
    )

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

    tipo_resultado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    datos: Mapped[dict | list | float | int] = mapped_column(
        JSON,
        nullable=False,
    )

    operacion = relationship(
        "Operacion",
        back_populates="resultado",
    )