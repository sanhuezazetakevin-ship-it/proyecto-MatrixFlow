import cv2
import numpy as np

from sqlalchemy.orm import Session

from app.models.persona_model import Persona
from app.models.face_embedding_model import FaceEmbedding
from app.models.recognition_model import RecognitionLog

from app.services.embedding_service import embedding_service
from app.services.similarity_service import cosine_similarity
from app.services.probability_service import probability_service


DEFAULT_THRESHOLD = 0.75


class RecognitionService:

    def recognize(
        self,
        image_bytes: bytes,
        db: Session,
        threshold: float = DEFAULT_THRESHOLD
    ):
        """
        Reconoce un rostro comparándolo con los rostros
        registrados de personas activas.
        """

        # 1. Validar imagen
        if not image_bytes:
            raise ValueError(
                "No se recibió ninguna imagen."
            )

        # 2. Convertir bytes a imagen OpenCV
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

        # 3. Generar embedding
        try:

            captured_embedding = (
                embedding_service.generate_embedding(
                    image
                )
            )

        except ValueError as e:

            raise ValueError(str(e))

        if captured_embedding is None:
            raise ValueError(
                "No se pudo obtener un embedding facial."
            )

        # 4. Obtener embeddings registrados
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

        # 5. Buscar la mayor similitud
        best_persona = None
        best_similarity = -1.0

        for face_embedding, persona in registered_embeddings:

            stored_embedding = face_embedding.embedding

            if stored_embedding is None:
                continue

            try:

                stored_embedding = np.asarray(
                    stored_embedding,
                    dtype=np.float32
                )

                similarity = cosine_similarity(
                    captured_embedding,
                    stored_embedding
                )

            except Exception:
                continue

            if similarity > best_similarity:

                best_similarity = similarity
                best_persona = persona

        if best_persona is None:
            raise ValueError(
                "No se pudieron comparar los rostros registrados."
            )

        # 6. Calcular distancia
        distance = 1.0 - best_similarity

        # 7. Aplicar umbral
        coincide = (
            best_similarity >= threshold
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

        # 8. Probabilidad calibrada
        probability = None

        if probability_service.trained:

            probability = (
                probability_service.predict(
                    similitud=float(best_similarity),
                    calidad_imagen=0.0,
                    iluminacion=0.0
                )
            )

        # 9. Guardar auditoría
        log = RecognitionLog(
            persona_id=persona_id,
            similitud=float(best_similarity),
            distancia=float(distance),
            umbral=float(threshold),
            coincide=coincide,
            probabilidad_calibrada=probability
        )

        db.add(log)
        db.commit()
        db.refresh(log)

        # 10. Resultado
        return {
            "persona_id": persona_id,
            "nombre": nombre,
            "similitud": float(best_similarity),
            "distancia": float(distance),
            "umbral": float(threshold),
            "coincide": coincide,
            "probabilidad_calibrada": probability
        }


recognition_service = RecognitionService()