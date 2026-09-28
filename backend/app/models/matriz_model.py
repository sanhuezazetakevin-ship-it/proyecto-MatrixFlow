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


class Matriz(Base):
    __tablename__ = "matrices"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    filas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    columnas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
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

    valores = relationship(
        "MatrizValor",
        back_populates="matriz",
        cascade="all, delete-orphan",
        order_by="MatrizValor.id",
    )