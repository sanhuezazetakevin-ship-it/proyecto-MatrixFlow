from sqlalchemy.orm import Session

from app.models.audit_log_model import AuditLog


def registrar_auditoria(
    db: Session,
    usuario_id: int | None,
    accion: str,
    entidad: str,
    entidad_id: int | None = None,
    detalle: dict | None = None,
) -> None:
    """
    Agrega un registro de auditoría a la sesión actual.

    No hace commit: se guarda junto con la operación
    principal. Si esa operación falla y hace rollback,
    el registro de auditoría tampoco queda guardado.
    """
    db.add(
        AuditLog(
            usuario_id=usuario_id,
            accion=accion,
            entidad=entidad,
            entidad_id=entidad_id,
            detalle=detalle,
        )
    )
