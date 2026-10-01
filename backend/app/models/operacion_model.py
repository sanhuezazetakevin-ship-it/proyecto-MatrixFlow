from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.connection import Base


class Operacion(Base):
    __tablename__ = "operaciones"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
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

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="COMPLETADA",
        index=True,
    )

    mensaje_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    entradas = relationship(
        "OperacionEntrada",
        back_populates="operacion",
        cascade="all, delete-orphan",
        order_by="OperacionEntrada.orden",
    )

    resultado = relationship(
        "OperacionResultado",
        back_populates="operacion",
        uselist=False,
        cascade="all, delete-orphan",
    )