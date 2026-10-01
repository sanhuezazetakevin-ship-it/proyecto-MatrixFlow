import pytest

from app.models.audit_model import AuditLog
from app.services.audit_service import audit_service


class FakeSession:
    def __init__(self):
        self.added = []

    def add(self, obj):
        self.added.append(obj)


def test_registrar_auditoria():
    db = FakeSession()

    registro = audit_service.registrar(
        db=db,
        usuario_id=10,
        accion="crear",
        entidad="producto",
        entidad_id=25,
        detalle="Producto creado",
    )

    assert isinstance(registro, AuditLog)

    assert registro.usuario_id == 10
    assert registro.accion == "CREAR"
    assert registro.entidad == "producto"
    assert registro.entidad_id == "25"
    assert registro.detalle == "Producto creado"

    assert len(db.added) == 1
    assert db.added[0] is registro


def test_registrar_sin_usuario():
    db = FakeSession()

    registro = audit_service.registrar(
        db=db,
        accion="LOGIN_FALLIDO",
        entidad="auth",
        detalle="Intento de autenticación fallido",
    )

    assert registro.usuario_id is None
    assert registro.entidad_id is None
    assert registro.accion == "LOGIN_FALLIDO"


def test_normaliza_accion_y_entidad():
    db = FakeSession()

    registro = audit_service.registrar(
        db=db,
        accion="  actualizar  ",
        entidad="  PRODUCTO  ",
    )

    assert registro.accion == "ACTUALIZAR"
    assert registro.entidad == "producto"


def test_rechaza_accion_vacia():
    db = FakeSession()

    with pytest.raises(
        ValueError,
        match="acción",
    ):
        audit_service.registrar(
            db=db,
            accion="   ",
            entidad="producto",
        )


def test_rechaza_entidad_vacia():
    db = FakeSession()

    with pytest.raises(
        ValueError,
        match="entidad",
    ):
        audit_service.registrar(
            db=db,
            accion="CREAR",
            entidad="   ",
        )