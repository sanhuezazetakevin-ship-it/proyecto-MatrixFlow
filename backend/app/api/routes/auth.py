from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status
)
import cv2
import numpy as np
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.auth_schema import (
    LoginResponse,
    RegisterRequest,
    UserResponse
)

from app.services.auth_service import (
    auth_service,
    FACE_LOGIN_THRESHOLD
)

from app.core.security import (
    create_access_token,
    get_current_user
)
from app.services.embedding_service import (
    embedding_service
)
from app.models.usuario_model import Usuario
from app.services.liveness_service import liveness_service


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"]
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}


async def _read_face_upload(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Solo se permiten imágenes JPEG o PNG.")
    data = await file.read()
    if not data:
        raise ValueError("La captura está vacía.")
    if len(data) > MAX_IMAGE_SIZE:
        raise ValueError("La captura supera el tamaño máximo permitido de 5 MB.")
    return data


# ============================================================
# LOGIN TRADICIONAL
# ============================================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:

        usuario = auth_service.login(
            email=form_data.username,
            password=form_data.password,
            db=db
        )

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "rol": usuario.rol
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )


# ============================================================
# LOGIN FACIAL SIMPLE POR DNI
# ============================================================

@router.post(
    "/login-facial",
    response_model=LoginResponse
)
async def login_facial(
    dni: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:

        # ----------------------------------------------------
        # 1. Leer imagen
        # ----------------------------------------------------

        image_bytes = await _read_face_upload(file)

        # ----------------------------------------------------
        # 2. Verificar DNI + rostro
        # ----------------------------------------------------

        resultado = auth_service.login_facial(
            dni=dni,
            image_bytes=image_bytes,
            db=db,
            threshold=FACE_LOGIN_THRESHOLD
        )

        usuario = resultado["usuario"]

        # ----------------------------------------------------
        # 3. Crear JWT
        # ----------------------------------------------------

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "rol": usuario.rol
            }
        )

        # ----------------------------------------------------
        # 4. Respuesta
        # ----------------------------------------------------

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "mensaje": "Inicio de sesión facial exitoso",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo completar el inicio de sesión facial."
        )


# ============================================================
# LOGIN FACIAL + LIVENESS
# ============================================================

@router.post("/login-facial-liveness")
async def login_facial_liveness(
    dni: str = Form(...),

    frame1: UploadFile = File(...),
    frame2: UploadFile = File(...),
    frame3: UploadFile = File(...),
    frame4: UploadFile = File(...),
    frame5: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    try:

        # ====================================================
        # 1. VALIDAR DNI
        # ====================================================

        dni = dni.strip()

        if len(dni) != 8 or not dni.isdigit():
            raise ValueError(
                "El DNI debe contener exactamente 8 dígitos."
            )

        # ====================================================
        # 2. LEER LOS 5 FRAMES
        # ====================================================

        uploaded_frames = [
            frame1,
            frame2,
            frame3,
            frame4,
            frame5
        ]

        images = []

        for uploaded_file in uploaded_frames:

            image_bytes = await _read_face_upload(uploaded_file)

            image = liveness_service.decode_image(
                image_bytes
            )

            images.append(image)

        # ====================================================
        # 3. COMPROBAR LIVENESS
        # ====================================================

        liveness_result = (
            liveness_service.verify_frames(
                images
            )
        )

        # ====================================================
        # MODO PRUEBAS
        #
        # Si falla, mostramos temporalmente:
        # - motivo
        # - pose_change
        #
        # Esto nos permitirá calibrar el sistema.
        # ====================================================

        if not liveness_result["liveness"]:

            pose_change = liveness_result.get(
                "pose_change",
                0.0
            )

            reason = liveness_result.get(
                "reason",
                "No se pudo verificar la presencia facial."
            )

            raise ValueError(
                f"{reason} "
                f"Pose change detectado: "
                f"{pose_change:.3f}"
            )

        # ====================================================
        # 4. OBTENER EMBEDDING DEL MEJOR FRAME
        # ====================================================

        captured_embedding = (
            liveness_result["best_embedding"]
        )

        # ====================================================
        # 5. VERIFICAR DNI + IDENTIDAD FACIAL
        # ====================================================

        resultado = (
            auth_service.login_facial_embedding(
                dni=dni,
                captured_embedding=captured_embedding,
                db=db,
                threshold=FACE_LOGIN_THRESHOLD
            )
        )

        usuario = resultado["usuario"]

        # ====================================================
        # 6. GENERAR JWT
        # ====================================================

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "rol": usuario.rol
            }
        )

        # ====================================================
        # 7. RESPUESTA
        # ====================================================

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "mensaje": (
                "Inicio de sesión facial "
                "con verificación de presencia exitoso"
            ),

            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at
            },

            # ================================================
            # DATOS TEMPORALES PARA CALIBRACIÓN
            # ================================================

            "biometria": {
                "similitud": resultado["similitud"],
                "umbral": resultado["umbral"],
                "pose_change": (
                    liveness_result["pose_change"]
                ),
                "detection_score": (
                    liveness_result["detection_score"]
                ),
                "face_ratio": (
                    liveness_result["face_ratio"]
                )
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail="No se pudo completar la autenticación facial."
        )

# ============================================================
# REGISTRO FACIAL COMPLETO
# ============================================================

@router.post(
    "/registro-facial",
    status_code=status.HTTP_201_CREATED
)
async def registro_facial(
    dni: str = Form(...),
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),

    frame1: UploadFile = File(...),
    frame2: UploadFile = File(...),
    frame3: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    try:

        # ====================================================
        # 1. VALIDACIONES
        # ====================================================

        dni = dni.strip()
        nombre = nombre.strip()
        email = email.strip().lower()

        if len(dni) != 8 or not dni.isdigit():
            raise ValueError(
                "El DNI debe contener exactamente 8 dígitos."
            )

        if not nombre:
            raise ValueError(
                "El nombre es obligatorio."
            )

        if len(password) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres."
            )

        # ====================================================
        # 2. PROCESAR LOS 3 FRAMES
        # ====================================================

        uploaded_frames = [
            frame1,
            frame2,
            frame3
        ]

        embeddings = []

        for uploaded_file in uploaded_frames:

            image_bytes = await _read_face_upload(uploaded_file)

            image_array = np.frombuffer(
                image_bytes,
                dtype=np.uint8
            )

            image = cv2.imdecode(
                image_array,
                cv2.IMREAD_COLOR
            )

            if image is None:
                raise ValueError(
                    "No se pudo procesar una de las capturas."
                )

            embedding = (
                embedding_service.generate_embedding(
                    image
                )
            )

            embeddings.append(
                embedding
            )

        # ====================================================
        # 3. CREAR PERSONA + USUARIO + EMBEDDINGS
        # ====================================================

        resultado = (
            auth_service.register_facial_user(
                dni=dni,
                nombre=nombre,
                email=email,
                password=password,
                captured_embeddings=embeddings,
                db=db
            )
        )

        usuario = resultado["usuario"]
        persona = resultado["persona"]

        # ====================================================
        # 4. GENERAR JWT
        # ====================================================

        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "rol": usuario.rol
            }
        )

        # ====================================================
        # 5. RESPUESTA
        # ====================================================

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "success": True,
            "mensaje":
                "Registro facial completado correctamente.",

            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "rol": usuario.rol,
                "activo": usuario.activo,
                "created_at": usuario.created_at
            },

            "persona": {
                "id": persona.id,
                "dni": persona.dni,
                "nombre": persona.nombre,
                "email": persona.email
            },

            "biometria": {
                "embeddings_registrados":
                    resultado["embeddings_registrados"]
            }
        }

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Error durante el registro facial: "
                f"{str(error)}"
            )
        )
# ============================================================
# REGISTRO
# ============================================================

@router.post(
    "/registro",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:

        usuario = auth_service.register_user(
            nombre=data.nombre,
            email=data.email,
            password=data.password,
            db=db
        )

        return usuario

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# ============================================================
# USUARIO ACTUAL
# ============================================================

@router.get("/me")
def obtener_usuario_actual(
    current_user: Usuario = Depends(
        get_current_user
    )
):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "rol": current_user.rol,
        "activo": current_user.activo
    }