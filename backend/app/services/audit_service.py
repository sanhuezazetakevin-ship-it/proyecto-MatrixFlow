from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit_model import AuditLog


class AuditService:

    def registrar(
        self,
        db: Session,
        accion: str,
        entidad: str,
        usuario_id: Optional[int] = None,
        entidad_id: Optional[str | int] = None,
        detalle: Optional[str] = None,
    ) -> AuditLog:
        """
        Registra una acción en el historial de auditoría.

        Importante:
        - No realiza commit.
        - La transacción debe ser confirmada por el servicio principal.
        - Esto permite que la auditoría forme parte de la misma transacción.
        """

        accion_normalizada = accion.strip().upper()
        entidad_normalizada = entidad.strip().lower()

        if not accion_normalizada:
            raise ValueError("La acción de auditoría es obligatoria.")

        if not entidad_normalizada:
            raise ValueError("La entidad de auditoría es obligatoria.")

        registro = AuditLog(
            usuario_id=usuario_id,
            accion=accion_normalizada,
            entidad=entidad_normalizada,
            entidad_id=(
                str(entidad_id)
                if entidad_id is not None
                else None
            ),
            detalle=detalle,
        )

        db.add(registro)

        return registro

    def listar(
        self,
        db: Session,
        limite: int = 100,
    ) -> list[AuditLog]:
        """
        Obtiene los registros más recientes.
        """

        limite = max(1, min(limite, 500))

        return (
            db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .limit(limite)
            .all()
        )

    def listar_por_usuario(
        self,
        usuario_id: int,
        db: Session,
        limite: int = 100,
    ) -> list[AuditLog]:

        limite = max(1, min(limite, 500))

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.usuario_id == usuario_id
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limite)
            .all()
        )

    def listar_por_entidad(
        self,
        entidad: str,
        db: Session,
        limite: int = 100,
    ) -> list[AuditLog]:

        entidad_normalizada = entidad.strip().lower()

        if not entidad_normalizada:
            raise ValueError(
                "La entidad es obligatoria."
            )

        limite = max(1, min(limite, 500))

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.entidad == entidad_normalizada
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limite)
            .all()
        )


audit_service = AuditService()