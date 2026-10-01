from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

import cv2
import numpy as np

from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    require_role,
)
from app.database.connection import get_db

from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding
from app.models.usuario_model import Usuario

from app.schemas.persona_schema import (
    PersonaCreate,
    PersonaResponse,
)

from app.services.embedding_service import embedding_service
from app.services.audit_service import audit_service


router = APIRouter(
    prefix="/api/personas",
    tags=["Personas"],
)


# ============================================================
# FUNCIÓN AUXILIAR
# Verifica si el usuario puede acceder a una persona
# ============================================================

def verificar_acceso_persona(
    persona_id: int,
    current_user: Usuario,
) -> None:

    rol = (current_user.rol or "").strip().lower()

    # El administrador puede acceder a cualquier persona
    if rol == "administrador":
        return

    # Los demás usuarios solamente pueden acceder
    # a la Persona vinculada con su cuenta.
    if current_user.persona_id != persona_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a esta persona.",
        )


# ============================================================
# CREAR PERSONA
# operador / administrador
# ============================================================

@router.post(
    "/",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_persona(
    persona: PersonaCreate,
    current_user: Usuario = Depends(
        require_role(
            "operador",
            "administrador",
        )
    ),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # 1. Verificar DNI
    # --------------------------------------------------------

    persona_existente = (
        db.query(Persona)
        .filter(
            Persona.dni == persona.dni
        )
        .first()
    )

    if persona_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DNI ya está registrado.",
        )

    # --------------------------------------------------------
    # 2. Crear persona
    # --------------------------------------------------------

    nueva_persona = Persona(
        dni=persona.dni,
        nombre=persona.nombre,
        email=persona.email,
    )

    db.add(nueva_persona)

    try:

        # Necesitamos el ID antes del commit
        db.flush()

        # ----------------------------------------------------
        # 3. Auditoría
        # ----------------------------------------------------

        audit_service.registrar(
            db=db,
            usuario_id=current_user.id,
            accion="CREAR",
            entidad="persona",
            entidad_id=nueva_persona.id,
            detalle="Persona registrada.",
        )

        # Persona + auditoría en una misma transacción
        db.commit()

        db.refresh(nueva_persona)

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo registrar la persona.",
        )

    return nueva_persona


# ============================================================
# LISTAR PERSONAS
# operador / administrador
# ============================================================

@router.get(
    "/",
    response_model=list[PersonaResponse],
)
def listar_personas(
    current_user: Usuario = Depends(
        require_role(
            "operador",
            "administrador",
        )
    ),
    db: Session = Depends(get_db),
):

    return (
        db.query(Persona)
        .order_by(Persona.id.asc())
        .all()
    )


# ============================================================
# REGISTRAR ROSTRO
#
# administrador -> cualquier persona
# usuario       -> solamente su propia persona
# ============================================================

@router.post(
    "/{persona_id}/rostro",
)
async def registrar_rostro(
    persona_id: int,
    file: UploadFile = File(...),
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # 1. Verificar permisos
    # --------------------------------------------------------

    verificar_acceso_persona(
        persona_id=persona_id,
        current_user=current_user,
    )

    # --------------------------------------------------------
    # 2. Buscar persona
    # --------------------------------------------------------

    persona = (
        db.query(Persona)
        .filter(
            Persona.id == persona_id
        )
        .first()
    )

    if persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada.",
        )

    # --------------------------------------------------------
    # 3. Verificar estado
    # --------------------------------------------------------

    if not persona.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La persona está inactiva.",
        )

    # --------------------------------------------------------
    # 4. Validar archivo
    # --------------------------------------------------------

    if file.content_type not in {
        "image/jpeg",
        "image/png",
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten imágenes JPEG o PNG.",
        )

    # --------------------------------------------------------
    # 5. Leer imagen
    # --------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen está vacía.",
        )

    # Máximo aproximado: 5 MB
    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="La imagen supera el tamaño máximo permitido.",
        )

    # --------------------------------------------------------
    # 6. Convertir imagen
    # --------------------------------------------------------

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8,
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo leer la imagen recibida.",
        )

    # --------------------------------------------------------
    # 7. Generar embedding
    # --------------------------------------------------------

    try:

        embedding = (
            embedding_service.generate_embedding(
                image
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception:

        # No exponemos errores internos de OpenCV,
        # InsightFace, ONNX Runtime, etc.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar el rostro.",
        )

    # --------------------------------------------------------
    # 8. Preparar embedding
    # --------------------------------------------------------

    embedding_list = embedding.tolist()

    nuevo_embedding = FaceEmbedding(
        persona_id=persona_id,
        embedding=embedding_list,
        modelo="buffalo_l",
    )

    db.add(nuevo_embedding)

    try:

        # Obtener ID sin confirmar la transacción
        db.flush()

        # ----------------------------------------------------
        # 9. Auditoría
        # ----------------------------------------------------

        audit_service.registrar(
            db=db,
            usuario_id=current_user.id,
            accion="REGISTRAR_ROSTRO",
            entidad="persona",
            entidad_id=persona_id,
            detalle="Embedding facial registrado.",
        )

        # Embedding + auditoría juntos
        db.commit()

        db.refresh(nuevo_embedding)

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo guardar el registro facial.",
        )

    # --------------------------------------------------------
    # 10. Respuesta
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Rostro registrado correctamente.",
        "persona_id": persona_id,
        "embedding_id": nuevo_embedding.id,
        "modelo": nuevo_embedding.modelo,
        "dimension": len(embedding_list),
    }


# ============================================================
# OBTENER PERSONA
#
# administrador -> cualquier persona
# usuario       -> solamente su propia persona
# ============================================================

@router.get(
    "/{persona_id}",
    response_model=PersonaResponse,
)
def obtener_persona(
    persona_id: int,
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    verificar_acceso_persona(
        persona_id=persona_id,
        current_user=current_user,
    )

    persona = (
        db.query(Persona)
        .filter(
            Persona.id == persona_id
        )
        .first()
    )

    if persona is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona no encontrada.",
        )

    return persona