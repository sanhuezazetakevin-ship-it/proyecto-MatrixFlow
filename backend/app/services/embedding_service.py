from insightface.app import FaceAnalysis
import numpy as np


class EmbeddingService:

    def __init__(self):
        self.model = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.model.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def generate_embedding(self, image: np.ndarray) -> np.ndarray:
        """
        Detecta un único rostro y genera su embedding facial.
        """

        if image is None:
            raise ValueError("La imagen recibida es inválida")

        faces = self.model.get(image)

        if len(faces) == 0:
            raise ValueError("No se detectó ningún rostro")

        if len(faces) > 1:
            raise ValueError(
                "Se detectaron varios rostros. "
                "Debe haber solamente uno."
            )

        embedding = faces[0].embedding

        if embedding is None:
            raise ValueError("No se pudo generar el embedding facial")

        return embedding.astype(np.float32)


# Instancia única del servicio
embedding_service = EmbeddingService()