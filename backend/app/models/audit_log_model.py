from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    accion: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    entidad: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    entidad_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    detalle: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
