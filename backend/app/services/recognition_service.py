import cv2
import numpy as np

from sqlalchemy.orm import Session

from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding
from app.models.recognition_model import RecognitionLog

from app.services.embedding_service import embedding_service
from app.services.similarity_service import (
    DEFAULT_FACE_THRESHOLD,
    normalize_embedding,
    is_match
)
from app.services.probability_service import probability_service


DEFAULT_THRESHOLD = DEFAULT_FACE_THRESHOLD


class RecognitionService:

    def recognize(
        self,
        image_bytes: bytes,
        db: Session,
        threshold: float = DEFAULT_THRESHOLD
    ) -> dict:
        """
        Reconoce un rostro comparándolo con los embeddings
        registrados de personas activas.
        """

        # =====================================================
        # 1. VALIDAR THRESHOLD
        # =====================================================

        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                "El threshold debe estar entre 0.0 y 1.0."
            )

        # =====================================================
        # 2. VALIDAR IMAGEN
        # =====================================================

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
                "No se pudo leer la imagen recibida."
            )

        # =====================================================
        # 3. GENERAR EMBEDDING
        # =====================================================

        captured_embedding = (
            embedding_service.generate_embedding(
                image
            )
        )

        captured_embedding = normalize_embedding(
            captured_embedding
        )

        # =====================================================
        # 4. OBTENER EMBEDDINGS REGISTRADOS
        # =====================================================

        registered_embeddings = (
            db.query(
                FaceEmbedding,
                Persona
            )
            .join(
                Persona,
                Persona.id == FaceEmbedding.persona_id
            )
            .filter(
                Persona.activo.is_(True)
            )
            .all()
        )

        if not registered_embeddings:
            raise ValueError(
                "No existen rostros registrados."
            )

        # =====================================================
        # 5. PREPARAR EMBEDDINGS VÁLIDOS
        # =====================================================

        valid_embeddings = []
        personas = []

        for face_embedding, persona in registered_embeddings:

            if face_embedding.embedding is None:
                continue

            try:

                normalized_embedding = (
                    normalize_embedding(
                        face_embedding.embedding
                    )
                )

            except (ValueError, TypeError):
                continue

            valid_embeddings.append(
                normalized_embedding
            )

            personas.append(
                persona
            )

        if not valid_embeddings:
            raise ValueError(
                "No existen embeddings faciales válidos."
            )

        # =====================================================
        # 6. COMPARACIÓN VECTORIZADA CON NUMPY
        # =====================================================

        embedding_matrix = np.stack(
            valid_embeddings
        )

        similarities = (
            embedding_matrix
            @ captured_embedding
        )

        best_index = int(
            np.argmax(
                similarities
            )
        )

        best_similarity = float(
            similarities[
                best_index
            ]
        )

        best_persona = personas[
            best_index
        ]

        # Protección numérica.
        best_similarity = float(
            np.clip(
                best_similarity,
                -1.0,
                1.0
            )
        )

        # =====================================================
        # 7. RESULTADO
        # =====================================================

        distance = float(
            1.0 - best_similarity
        )

        coincide = is_match(
            best_similarity,
            threshold
        )

        persona_id = (
            best_persona.id
            if coincide
            else None
        )

        nombre = (
            best_persona.nombre
            if coincide
            else None
        )

        # =====================================================
        # 8. PROBABILIDAD CALIBRADA
        # =====================================================

        probability = None

        if probability_service.trained:

            probability = (
                probability_service.predict(
                    similitud=best_similarity,
                    calidad_imagen=0.0,
                    iluminacion=0.0
                )
            )

        # =====================================================
        # 9. REGISTRAR RESULTADO
        # =====================================================

        log = RecognitionLog(
            persona_id=persona_id,
            similitud=best_similarity,
            distancia=distance,
            umbral=float(threshold),
            coincide=coincide,
            probabilidad_calibrada=probability
        )

        try:

            db.add(log)
            db.commit()
            db.refresh(log)

        except Exception:

            db.rollback()
            raise

        # =====================================================
        # 10. RESPUESTA
        # =====================================================

        return {
            "persona_id": persona_id,
            "nombre": nombre,
            "similitud": best_similarity,
            "distancia": distance,
            "umbral": float(threshold),
            "coincide": coincide,
            "probabilidad_calibrada": probability
        }


recognition_service = RecognitionService()