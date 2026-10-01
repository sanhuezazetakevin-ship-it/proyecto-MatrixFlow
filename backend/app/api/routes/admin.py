from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.services.audit_service import audit_service


router = APIRouter(
    prefix="/api/admin",
    tags=["Administración"],
)


# ============================================================
# CONFIGURACIÓN RBAC
# ============================================================

ROLES_PERMITIDOS = {
    "consulta",
    "operador",
    "administrador",
}


# ============================================================
# PRUEBA DE ACCESO ADMINISTRATIVO
# ============================================================

@router.get("/prueba")
def prueba_admin(
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
):
    return {
        "success": True,
        "mensaje": "Acceso administrativo autorizado",
        "usuario": current_user.nombre,
        "rol": current_user.rol,
    }


# ============================================================
# CAMBIAR ROL DE USUARIO
# ============================================================

@router.put("/usuarios/{usuario_id}/rol")
def cambiar_rol(
    usuario_id: int,
    nuevo_rol: str,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    nuevo_rol = nuevo_rol.strip().lower()

    if nuevo_rol not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Rol no válido. "
                "Use 'consulta', 'operador' "
                "o 'administrador'."
            ),
        )

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    # Evita que un administrador se quite
    # accidentalmente sus propios privilegios.
    if (
        usuario.id == current_user.id
        and nuevo_rol != "administrador"
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "No puedes quitarte a ti mismo "
                "el rol de administrador."
            ),
        )

    rol_anterior = usuario.rol
    usuario.rol = nuevo_rol

    try:
        audit_service.registrar(
            db=db,
            usuario_id=current_user.id,
            accion="CAMBIAR_ROL",
            entidad="usuario",
            entidad_id=usuario.id,
            detalle=f"Rol cambiado de {rol_anterior} a {nuevo_rol}.",
        )

        db.commit()
        db.refresh(usuario)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el rol del usuario.",
        )

    return {
        "success": True,
        "mensaje": "Rol actualizado correctamente",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "activo": usuario.activo,
        },
    }


# ============================================================
# ACTIVAR / DESACTIVAR USUARIO
# ============================================================

@router.put("/usuarios/{usuario_id}/estado")
def cambiar_estado_usuario(
    usuario_id: int,
    activo: bool,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    # El administrador no puede desactivar
    # accidentalmente su propia cuenta.
    if usuario.id == current_user.id and not activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta.",
        )

    usuario.activo = activo

    try:
        audit_service.registrar(
            db=db,
            usuario_id=current_user.id,
            accion="ACTIVAR" if activo else "DESACTIVAR",
            entidad="usuario",
            entidad_id=usuario.id,
            detalle=(
                "Cuenta de usuario activada."
                if activo
                else "Cuenta de usuario desactivada."
            ),
        )

        db.commit()
        db.refresh(usuario)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo actualizar el estado del usuario.",
        )

    return {
        "success": True,
        "mensaje": (
            "Usuario activado correctamente"
            if activo
            else "Usuario desactivado correctamente"
        ),
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "activo": usuario.activo,
        },
    }


# ============================================================
# LISTAR USUARIOS
# ============================================================

@router.get("/usuarios")
def listar_usuarios(
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    usuarios = (
        db.query(Usuario)
        .order_by(Usuario.id.asc())
        .all()
    )

    return {
        "success": True,
        "total": len(usuarios),
        "usuarios": [
            {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at,
            }
            for usuario in usuarios
        ],
    }


# ============================================================
# OBTENER USUARIO
# ============================================================

@router.get("/usuarios/{usuario_id}")
def obtener_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return {
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "created_at": usuario.created_at,
        },
    }