import pytest
from fastapi import HTTPException

from app.core.security import require_role


# ============================================================
# USUARIO FALSO PARA PRUEBAS
# ============================================================

class FakeUsuario:
    def __init__(self, rol: str):
        self.id = 1
        self.nombre = "Usuario Test"
        self.email = "test@matrixflow.com"
        self.rol = rol
        self.activo = True


# ============================================================
# FUNCIÓN AUXILIAR
# ============================================================

def ejecutar_permiso(roles_permitidos, rol_usuario):
    """
    Ejecuta directamente el verificador generado por require_role.
    """

    dependency = require_role(*roles_permitidos)

    usuario = FakeUsuario(rol_usuario)

    return dependency(usuario)


# ============================================================
# TESTS - ROL CONSULTA
# ============================================================

def test_consulta_puede_acceder_a_consulta():
    usuario = ejecutar_permiso(
        ("consulta",),
        "consulta",
    )

    assert usuario.rol == "consulta"


def test_consulta_no_puede_acceder_a_operador():
    with pytest.raises(HTTPException) as error:
        ejecutar_permiso(
            ("operador", "administrador"),
            "consulta",
        )

    assert error.value.status_code == 403


def test_consulta_no_puede_acceder_a_administrador():
    with pytest.raises(HTTPException) as error:
        ejecutar_permiso(
            ("administrador",),
            "consulta",
        )

    assert error.value.status_code == 403


# ============================================================
# TESTS - ROL OPERADOR
# ============================================================

def test_operador_puede_acceder_a_operaciones():
    usuario = ejecutar_permiso(
        ("operador", "administrador"),
        "operador",
    )

    assert usuario.rol == "operador"


def test_operador_no_puede_acceder_a_administracion():
    with pytest.raises(HTTPException) as error:
        ejecutar_permiso(
            ("administrador",),
            "operador",
        )

    assert error.value.status_code == 403


# ============================================================
# TESTS - ROL ADMINISTRADOR
# ============================================================

def test_administrador_puede_acceder_a_operaciones():
    usuario = ejecutar_permiso(
        ("operador", "administrador"),
        "administrador",
    )

    assert usuario.rol == "administrador"


def test_administrador_puede_acceder_a_administracion():
    usuario = ejecutar_permiso(
        ("administrador",),
        "administrador",
    )

    assert usuario.rol == "administrador"


# ============================================================
# TESTS - NORMALIZACIÓN
# ============================================================

def test_roles_no_distinguen_mayusculas():
    usuario = ejecutar_permiso(
        ("administrador",),
        "ADMINISTRADOR",
    )

    assert usuario.rol == "ADMINISTRADOR"


def test_roles_eliminan_espacios():
    usuario = ejecutar_permiso(
        ("operador",),
        "  operador  ",
    )

    assert usuario.rol == "  operador  "


# ============================================================
# TESTS - ROLES INVÁLIDOS
# ============================================================

def test_usuario_con_rol_invalido_es_rechazado():
    with pytest.raises(HTTPException) as error:
        ejecutar_permiso(
            ("administrador",),
            "admin",
        )

    assert error.value.status_code == 403


def test_usuario_sin_rol_es_rechazado():
    with pytest.raises(HTTPException) as error:
        ejecutar_permiso(
            ("administrador",),
            "",
        )

    assert error.value.status_code == 403


def test_require_role_rechaza_configuracion_invalida():
    with pytest.raises(ValueError):
        require_role("admin")


# ============================================================
# MATRIZ RBAC
# ============================================================

@pytest.mark.parametrize(
    "rol_usuario,roles_permitidos,debe_permitir",
    [
        # CONSULTA
        ("consulta", ("consulta",), True),
        ("consulta", ("operador", "administrador"), False),
        ("consulta", ("administrador",), False),

        # OPERADOR
        ("operador", ("operador", "administrador"), True),
        ("operador", ("administrador",), False),

        # ADMINISTRADOR
        ("administrador", ("administrador",), True),
        ("administrador", ("operador", "administrador"), True),
    ],
)
def test_matriz_rbac(
    rol_usuario,
    roles_permitidos,
    debe_permitir,
):
    if debe_permitir:
        usuario = ejecutar_permiso(
            roles_permitidos,
            rol_usuario,
        )

        assert usuario is not None

    else:
        with pytest.raises(HTTPException) as error:
            ejecutar_permiso(
                roles_permitidos,
                rol_usuario,
            )

        assert error.value.status_code == 403