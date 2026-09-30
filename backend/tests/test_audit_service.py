import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_audit.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

from app.services.audit_service import registrar_auditoria
from app.models.audit_log_model import AuditLog


class FakeSession:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


def test_registrar_auditoria_agrega_sin_commit():
    db = FakeSession()
    registrar_auditoria(
        db=db,
        usuario_id=7,
        accion="CREAR",
        entidad="venta",
        entidad_id=10,
        detalle={"total": "100.00"},
    )

    assert len(db.items) == 1
    log = db.items[0]
    assert isinstance(log, AuditLog)
    assert log.usuario_id == 7
    assert log.accion == "CREAR"
    assert log.entidad == "venta"
    assert log.entidad_id == 10
    assert log.detalle["total"] == "100.00"
