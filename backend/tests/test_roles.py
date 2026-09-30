import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_roles.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")

from app.core.security import normalizar_rol


def test_normaliza_roles_legacy():
    assert normalizar_rol("admin") == "administrador"
    assert normalizar_rol("ADMINISTRADOR") == "administrador"
    assert normalizar_rol("usuario") == "consulta"
    assert normalizar_rol(" consulta ") == "consulta"


def test_normaliza_rol_desconocido_sin_romper():
    assert normalizar_rol("otro") == "otro"
