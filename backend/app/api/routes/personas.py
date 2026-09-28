from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status
)
import cv2
import numpy as np
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding
from app.schemas.persona_schema import (
    PersonaCreate,
    PersonaResponse
)
from app.services.embedding_service import embedding_service
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(
    prefix="/api/personas",
    tags=["Personas"]
)

# ============================================================
# CREAR PERSONA
# ============================================================
@router.post(
    "/",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_persona(
    persona: PersonaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # --------------------------------------------------------
    # 1. Verificar que el DNI no exista
    # --------------------------------------------------------
    persona_existente = (
        db.query(Persona)
        .filter(Persona.dni == persona.dni)
        .first()
    )

    if persona_existente:
        raise HTTPException(
            status_code=400,
            detail="El DNI ya está registrado."
        )

    # --------------------------------------------------------
    # 2. Crear persona
    # --------------------------------------------------------

    nueva_persona = Persona(
        dni=persona.dni,
        nombre=persona.nombre,
        email=persona.email
    )

    db.add(nueva_persona)

    try:
        db.commit()
        db.refresh(nueva_persona)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="No se pudo registrar la persona. "
                    "Verifica que el DNI o email no estén registrados."
        )

    return nueva_persona


# ============================================================
# LISTAR PERSONAS
# ============================================================
@router.get(
    "/",
    response_model=list[PersonaResponse]
)
def listar_personas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(Persona)
        .order_by(Persona.id.asc())
        .all()
    )


# ============================================================
# REGISTRAR ROSTRO DE UNA PERSONA
# ============================================================
@router.post(
    "/{persona_id}/rostro"
)
async def registrar_rostro(
    persona_id: int,
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # --------------------------------------------------------
    # 1. Buscar persona
    # --------------------------------------------------------

    persona = (
        db.query(Persona)
        .filter(Persona.id == persona_id)
        .first()
    )

    if persona is None:
        raise HTTPException(
            status_code=404,
            detail="Persona no encontrada."
        )

    # --------------------------------------------------------
    # 2. Verificar que la persona esté activa
    # --------------------------------------------------------

    if not persona.activo:
        raise HTTPException(
            status_code=400,
            detail="La persona está inactiva."
        )

    # --------------------------------------------------------
    # 3. Leer imagen
    # --------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="La imagen está vacía."
        )

    # --------------------------------------------------------
    # 4. Convertir bytes a imagen OpenCV
    # --------------------------------------------------------

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="No se pudo leer la imagen recibida."
        )

    # --------------------------------------------------------
    # 5. Generar embedding facial
    # --------------------------------------------------------

    try:

        embedding = embedding_service.generate_embedding(
            image
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el rostro: {str(error)}"
        )

    # --------------------------------------------------------
    # 6. Convertir NumPy a lista Python
    # --------------------------------------------------------

    embedding_list = embedding.tolist()

    # --------------------------------------------------------
    # 7. Guardar embedding
    # --------------------------------------------------------

    nuevo_embedding = FaceEmbedding(
        persona_id=persona_id,
        embedding=embedding_list,
        modelo="buffalo_l"
    )

    db.add(nuevo_embedding)

    try:

        db.commit()
        db.refresh(nuevo_embedding)

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el embedding facial."
        )

    # --------------------------------------------------------
    # 8. Respuesta
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Rostro registrado correctamente.",
        "persona_id": persona_id,
        "embedding_id": nuevo_embedding.id,
        "modelo": nuevo_embedding.modelo,
        "dimension": len(embedding_list)
    }


# ============================================================
# OBTENER PERSONA
# ============================================================
@router.get(
    "/{persona_id}",
    response_model=PersonaResponse
)
def obtener_persona(
    persona_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    persona = (
        db.query(Persona)
        .filter(Persona.id == persona_id)
        .first()
    )
    if persona is None:
        raise HTTPException(
            status_code=404,
            detail="Persona no encontrada"
        )

    return persona