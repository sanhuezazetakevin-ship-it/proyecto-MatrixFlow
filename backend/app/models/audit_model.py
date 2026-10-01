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


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "usuarios.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    accion: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    entidad: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entidad_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    detalle: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )

    usuario = relationship(
        "Usuario",
    )