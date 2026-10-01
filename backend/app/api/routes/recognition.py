from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.core.security import (
    get_current_user,
    require_role,
)

from app.database.connection import get_db

from app.models.recognition_model import RecognitionLog
from app.models.usuario_model import Usuario

from app.schemas.recognition_schema import (
    RecognitionHistoryResponse,
    RecognitionResponse,
)

from app.services.recognition_service import (
    DEFAULT_THRESHOLD,
    recognition_service,
)


router = APIRouter(
    prefix="/api/reconocimiento",
    tags=["Reconocimiento"],
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
}


# ============================================================
# RECONOCER ROSTRO
# Todos los usuarios autenticados
# ============================================================

@router.post(
    "",
    response_model=RecognitionResponse,
)
async def reconocer_rostro(
    file: UploadFile = File(...),
    threshold: float = Form(DEFAULT_THRESHOLD),
    current_user: Usuario = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    # --------------------------------------------------------
    # 1. Validar threshold
    # --------------------------------------------------------

    if threshold < 0.50 or threshold > 0.95:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "El umbral debe estar entre "
                "0.50 y 0.95."
            ),
        )

    # --------------------------------------------------------
    # 2. Validar tipo de archivo
    # --------------------------------------------------------

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Solo se permiten imágenes "
                "JPEG o PNG."
            ),
        )

    # --------------------------------------------------------
    # 3. Leer imagen
    # --------------------------------------------------------

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se recibió ninguna imagen.",
        )

    # --------------------------------------------------------
    # 4. Validar tamaño
    # --------------------------------------------------------

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                "La imagen supera el tamaño "
                "máximo permitido de 5 MB."
            ),
        )

    # --------------------------------------------------------
    # 5. Ejecutar reconocimiento
    # --------------------------------------------------------

    try:

        resultado = recognition_service.recognize(
            image_bytes=image_bytes,
            db=db,
            threshold=threshold,
        )

        return resultado

    except ValueError as error:

        # Errores controlados del servicio:
        # imagen inválida, rostro no detectable, etc.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except HTTPException:
        raise

    except Exception as error:

        # El error completo queda únicamente
        # en la consola del backend.
        print(
            "ERROR INTERNO EN RECONOCIMIENTO:",
            repr(error),
        )

        # No exponemos información de:
        # InsightFace, OpenCV, SQLAlchemy,
        # PostgreSQL, rutas internas, etc.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "No se pudo completar "
                "el reconocimiento facial."
            ),
        )


# ============================================================
# HISTORIAL DE RECONOCIMIENTOS
# Solo administrador
# ============================================================

@router.get(
    "/historial",
    response_model=list[RecognitionHistoryResponse],
)
def historial_reconocimiento(
    current_user: Usuario = Depends(
        require_role("administrador")
    ),
    db: Session = Depends(get_db),
):

    registros = (
        db.query(RecognitionLog)
        .order_by(
            RecognitionLog.created_at.desc()
        )
        .all()
    )

    return registros