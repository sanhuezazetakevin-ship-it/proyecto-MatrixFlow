from sqlalchemy.orm import Session
from passlib.context import CryptContext

import cv2
import numpy as np

from app.models.usuario_model import Usuario
from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding

from app.services.embedding_service import embedding_service
from app.services.similarity_service import cosine_similarity


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


FACE_LOGIN_THRESHOLD = 0.75


class AuthService:

    # ========================================================
    # PASSWORD
    # ========================================================

    def hash_password(
        self,
        password: str
    ) -> str:
        return pwd_context.hash(password)

    def verify_password(
        self,
        password: str,
        password_hash: str
    ) -> bool:
        return pwd_context.verify(
            password,
            password_hash
        )

    # ========================================================
    # REGISTRO TRADICIONAL
    # ========================================================

    def register_user(
        self,
        nombre: str,
        email: str,
        password: str,
        db: Session
    ):
        email = email.strip().lower()

        usuario_existente = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario_existente:
            raise ValueError(
                "Ya existe un usuario con ese correo."
            )

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=self.hash_password(
                password
            ),
            rol="consulta",
            activo=True
        )

        db.add(nuevo_usuario)

        try:
            db.commit()
            db.refresh(nuevo_usuario)

        except Exception:
            db.rollback()
            raise

        return nuevo_usuario

    # ========================================================
    # LOGIN TRADICIONAL
    # ========================================================

    def login(
        self,
        email: str,
        password: str,
        db: Session
    ):
        email = email.strip().lower()

        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario is None:
            raise ValueError(
                "Correo o contraseña incorrectos."
            )

        if not usuario.activo:
            raise ValueError(
                "El usuario está desactivado."
            )

        if not self.verify_password(
            password,
            usuario.password_hash
        ):
            raise ValueError(
                "Correo o contraseña incorrectos."
            )

        return usuario

    # ========================================================
    # LOGIN FACIAL POR DNI + IMAGEN
    # ========================================================

    def login_facial(
        self,
        dni: str,
        image_bytes: bytes,
        db: Session,
        threshold: float = FACE_LOGIN_THRESHOLD
    ):
        # ----------------------------------------------------
        # 1. Validar DNI
        # ----------------------------------------------------

        dni = dni.strip()

        if len(dni) != 8 or not dni.isdigit():
            raise ValueError(
                "El DNI debe contener exactamente 8 dígitos."
            )

        # ----------------------------------------------------
        # 2. Buscar persona
        # ----------------------------------------------------

        persona = (
            db.query(Persona)
            .filter(Persona.dni == dni)
            .first()
        )

        if persona is None or not persona.activo:
            raise ValueError(
                "No se pudo verificar la identidad."
            )

        # ----------------------------------------------------
        # 3. Buscar usuario vinculado
        # ----------------------------------------------------

        usuario = (
            db.query(Usuario)
            .filter(
                Usuario.persona_id == persona.id
            )
            .first()
        )

        if usuario is None:
            raise ValueError(
                "No existe una cuenta vinculada "
                "a esta identidad."
            )

        if not usuario.activo:
            raise ValueError(
                "La cuenta está desactivada."
            )

        # ----------------------------------------------------
        # 4. Obtener embeddings
        # ----------------------------------------------------

        embeddings = (
            db.query(FaceEmbedding)
            .filter(
                FaceEmbedding.persona_id
                == persona.id
            )
            .all()
        )

        if not embeddings:
            raise ValueError(
                "La identidad no tiene "
                "un rostro registrado."
            )

        # ----------------------------------------------------
        # 5. Procesar imagen
        # ----------------------------------------------------

        if not image_bytes:
            raise ValueError(
                "No se recibió ninguna imagen."
            )

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
                "No se pudo leer la imagen."
            )

        # ----------------------------------------------------
        # 6. Generar embedding
        # ----------------------------------------------------

        captured_embedding = (
            embedding_service.generate_embedding(
                image
            )
        )

        # ----------------------------------------------------
        # 7. Comparar embedding
        # ----------------------------------------------------

        best_similarity = (
            self._compare_embeddings(
                captured_embedding=
                    captured_embedding,
                registered_embeddings=
                    embeddings
            )
        )

        # ----------------------------------------------------
        # 8. Validar similitud
        # ----------------------------------------------------

        if best_similarity < threshold:
            raise ValueError(
                "No se pudo verificar la identidad."
            )

        # ----------------------------------------------------
        # 9. Resultado
        # ----------------------------------------------------

        return {
            "usuario": usuario,
            "persona": persona,
            "similitud": float(
                best_similarity
            ),
            "umbral": float(threshold)
        }

    # ========================================================
    # LOGIN FACIAL CON EMBEDDING YA GENERADO
    # ========================================================

    def login_facial_embedding(
        self,
        dni: str,
        captured_embedding: np.ndarray,
        db: Session,
        threshold: float = FACE_LOGIN_THRESHOLD
    ):
        """
        Este método se utiliza después del liveness.

        El LivenessService ya analizó los frames y generó
        el embedding del mejor frame, por lo que aquí no
        volvemos a procesar ninguna imagen.
        """

        # ----------------------------------------------------
        # 1. Validar DNI
        # ----------------------------------------------------

        dni = dni.strip()

        if len(dni) != 8 or not dni.isdigit():
            raise ValueError(
                "El DNI debe contener exactamente 8 dígitos."
            )

        # ----------------------------------------------------
        # 2. Buscar persona
        # ----------------------------------------------------

        persona = (
            db.query(Persona)
            .filter(Persona.dni == dni)
            .first()
        )

        if persona is None or not persona.activo:
            raise ValueError(
                "No se pudo verificar la identidad."
            )

        # ----------------------------------------------------
        # 3. Buscar usuario vinculado
        # ----------------------------------------------------

        usuario = (
            db.query(Usuario)
            .filter(
                Usuario.persona_id == persona.id
            )
            .first()
        )

        if usuario is None:
            raise ValueError(
                "No existe una cuenta vinculada "
                "a esta identidad."
            )

        if not usuario.activo:
            raise ValueError(
                "La cuenta está desactivada."
            )

        # ----------------------------------------------------
        # 4. Obtener embeddings registrados
        # ----------------------------------------------------

        embeddings = (
            db.query(FaceEmbedding)
            .filter(
                FaceEmbedding.persona_id
                == persona.id
            )
            .all()
        )

        if not embeddings:
            raise ValueError(
                "La identidad no tiene "
                "un rostro registrado."
            )

        # ----------------------------------------------------
        # 5. Validar embedding capturado
        # ----------------------------------------------------

        if captured_embedding is None:
            raise ValueError(
                "No se recibió un embedding facial."
            )

        captured_embedding = np.asarray(
            captured_embedding,
            dtype=np.float32
        )

        if captured_embedding.size == 0:
            raise ValueError(
                "El embedding facial capturado "
                "es inválido."
            )

        if captured_embedding.ndim != 1:
            captured_embedding = (
                captured_embedding.flatten()
            )

        # InsightFace buffalo_l genera 512 dimensiones
        if captured_embedding.shape[0] != 512:
            raise ValueError(
                "El embedding facial tiene "
                "una dimensión inválida."
            )

        # ----------------------------------------------------
        # 6. Comparar embeddings
        # ----------------------------------------------------

        best_similarity = (
            self._compare_embeddings(
                captured_embedding=
                    captured_embedding,
                registered_embeddings=
                    embeddings
            )
        )

        # ----------------------------------------------------
        # 7. Validar umbral
        # ----------------------------------------------------

        if best_similarity < threshold:
            raise ValueError(
                "No se pudo verificar la identidad."
            )

        # ----------------------------------------------------
        # 8. Resultado
        # ----------------------------------------------------

        return {
            "usuario": usuario,
            "persona": persona,
            "similitud": float(
                best_similarity
            ),
            "umbral": float(threshold)
        }
    # ========================================================
    # REGISTRO DE USUARIO + PERSONA + ROSTROS
    # ========================================================

    def register_facial_user(
        self,
        dni: str,
        nombre: str,
        email: str,
        password: str,
        captured_embeddings: list[np.ndarray],
        db: Session
    ):
        # ----------------------------------------------------
        # 1. Normalizar datos
        # ----------------------------------------------------

        dni = dni.strip()
        nombre = nombre.strip()
        email = email.strip().lower()

        # ----------------------------------------------------
        # 2. Validaciones básicas
        # ----------------------------------------------------

        if len(dni) != 8 or not dni.isdigit():
            raise ValueError(
                "El DNI debe contener exactamente 8 dígitos."
            )

        if not nombre:
            raise ValueError(
                "El nombre es obligatorio."
            )

        if not email:
            raise ValueError(
                "El correo es obligatorio."
            )

        if len(password) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres."
            )

        if len(captured_embeddings) < 3:
            raise ValueError(
                "Se necesitan al menos 3 capturas faciales."
            )

        # ----------------------------------------------------
        # 3. Comprobar duplicados
        # ----------------------------------------------------

        persona_dni = (
            db.query(Persona)
            .filter(Persona.dni == dni)
            .first()
        )

        if persona_dni:
            raise ValueError(
                "El DNI ya está registrado."
            )

        persona_email = (
            db.query(Persona)
            .filter(Persona.email == email)
            .first()
        )

        if persona_email:
            raise ValueError(
                "El correo ya está registrado."
            )

        usuario_existente = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario_existente:
            raise ValueError(
                "El correo ya está asociado a una cuenta."
            )

        # ----------------------------------------------------
        # 4. Validar embeddings antes de escribir en BD
        # ----------------------------------------------------

        valid_embeddings: list[np.ndarray] = []

        for embedding in captured_embeddings:

            array = np.asarray(
                embedding,
                dtype=np.float32
            ).flatten()

            if array.shape[0] != 512:
                raise ValueError(
                    "Una de las capturas faciales es inválida."
                )

            valid_embeddings.append(array)

        # ----------------------------------------------------
        # 5. Crear Persona
        # ----------------------------------------------------

        nueva_persona = Persona(
            dni=dni,
            nombre=nombre,
            email=email,
            activo=True
        )

        try:
            db.add(nueva_persona)

            # Necesitamos el ID sin hacer commit todavía.
            db.flush()

            # ------------------------------------------------
            # 6. Crear Usuario vinculado
            # ------------------------------------------------

            nuevo_usuario = Usuario(
                persona_id=nueva_persona.id,
                nombre=nombre,
                email=email,
                password_hash=self.hash_password(
                    password
                ),
                rol="consulta",
                activo=True
            )

            db.add(nuevo_usuario)

            # ------------------------------------------------
            # 7. Guardar embeddings
            # ------------------------------------------------

            for embedding in valid_embeddings:

                nuevo_embedding = FaceEmbedding(
                    persona_id=nueva_persona.id,
                    embedding=embedding.tolist(),
                    modelo="buffalo_l"
                )

                db.add(nuevo_embedding)

            # ------------------------------------------------
            # 8. Una sola transacción
            # ------------------------------------------------

            db.commit()

            db.refresh(nueva_persona)
            db.refresh(nuevo_usuario)

        except ValueError:
            db.rollback()
            raise

        except Exception as error:
            db.rollback()

            raise ValueError(
                "No se pudo completar el registro."
            ) from error

        return {
            "usuario": nuevo_usuario,
            "persona": nueva_persona,
            "embeddings_registrados":
                len(valid_embeddings)
        }
    # ========================================================
    # COMPARACIÓN INTERNA DE EMBEDDINGS
    # ========================================================


    def _compare_embeddings(
        self,
        captured_embedding: np.ndarray,
        registered_embeddings: list
    ) -> float:

        captured_embedding = np.asarray(
            captured_embedding,
            dtype=np.float32
        ).flatten()

        best_similarity = -1.0

        for registered in registered_embeddings:

            if registered.embedding is None:
                continue

            stored_embedding = np.asarray(
                registered.embedding,
                dtype=np.float32
            ).flatten()

            # Ambos deben tener la misma dimensión
            if (
                stored_embedding.shape
                != captured_embedding.shape
            ):
                continue

            similarity = cosine_similarity(
                captured_embedding,
                stored_embedding
            )

            if similarity > best_similarity:
                best_similarity = similarity

        if best_similarity < 0:
            raise ValueError(
                "No se pudieron comparar "
                "los datos faciales."
            )

        return float(best_similarity)


# ============================================================
# SINGLETON
# ============================================================

auth_service = AuthService()