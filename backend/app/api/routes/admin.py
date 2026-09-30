from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database.connection import get_db
from app.models.usuario_model import Usuario
from app.models.audit_log_model import AuditLog
from app.services.audit_service import registrar_auditoria


router = APIRouter(
    prefix="/api/admin",
    tags=["Administración"]
)


@router.get("/prueba")
def prueba_admin(
    current_user: Usuario = Depends(
        require_role("administrador")
    )
):
    return {
        "success": True,
        "mensaje": "Acceso autorizado",
        "usuario": current_user.nombre,
        "rol": current_user.rol
    }


@router.put("/usuarios/{usuario_id}/rol")
def cambiar_rol(
    usuario_id: int,
    nuevo_rol: str,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db)
):

    roles_permitidos = ["administrador", "analista", "consulta"]

    if nuevo_rol not in roles_permitidos:
        raise HTTPException(
        status_code=400,
        detail="Rol no válido. Use 'administrador', 'analista' o 'consulta'."
    )

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario.id == current_user.id and nuevo_rol != "administrador":
        raise HTTPException(
            status_code=400,
            detail="No puede quitarse a sí mismo el rol de administrador."
        )

    rol_anterior = usuario.rol
    usuario.rol = nuevo_rol
    registrar_auditoria(
        db=db, usuario_id=current_user.id, accion="CAMBIAR_ROL",
        entidad="usuario", entidad_id=usuario.id,
        detalle={"rol_anterior": rol_anterior, "rol_nuevo": nuevo_rol},
    )
    db.commit()
    db.refresh(usuario)

    return {
        "success": True,
        "mensaje": "Rol actualizado correctamente",
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "activo": usuario.activo
        }
    }


@router.put("/usuarios/{usuario_id}/estado")
def cambiar_estado_usuario(
    usuario_id: int,
    activo: bool,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario.id == current_user.id and not activo:
        raise HTTPException(
            status_code=400,
            detail="No puede desactivarse a sí mismo."
        )

    estado_anterior = usuario.activo
    usuario.activo = activo
    registrar_auditoria(
        db=db, usuario_id=current_user.id, accion="CAMBIAR_ESTADO",
        entidad="usuario", entidad_id=usuario.id,
        detalle={"activo_anterior": estado_anterior, "activo_nuevo": activo},
    )
    db.commit()
    db.refresh(usuario)

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
            "activo": usuario.activo
        }
    }


@router.get("/usuarios")
def listar_usuarios(
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db)
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
                "created_at": usuario.created_at
            }
            for usuario in usuarios
        ]
    }


@router.get("/usuarios/{usuario_id}")
def obtener_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "created_at": usuario.created_at
        }
    }


@router.get("/auditoria")
def listar_auditoria(
    entidad: str | None = Query(default=None),
    accion: str | None = Query(default=None),
    usuario_id: int | None = Query(default=None),
    limite: int = Query(default=50, ge=1, le=200),
    desde: int = Query(default=0, ge=0),
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db)
):

    query = db.query(AuditLog)

    if entidad:
        query = query.filter(
            AuditLog.entidad == entidad.strip().lower()
        )

    if accion:
        query = query.filter(
            AuditLog.accion == accion.strip().upper()
        )

    if usuario_id is not None:
        query = query.filter(
            AuditLog.usuario_id == usuario_id
        )

    total = query.count()

    registros = (
        query
        .order_by(AuditLog.fecha.desc())
        .offset(desde)
        .limit(limite)
        .all()
    )

    return {
        "success": True,
        "total": total,
        "registros": [
            {
                "id": registro.id,
                "usuario_id": registro.usuario_id,
                "accion": registro.accion,
                "entidad": registro.entidad,
                "entidad_id": registro.entidad_id,
                "detalle": registro.detalle,
                "fecha": registro.fecha
            }
            for registro in registros
        ]
    }
