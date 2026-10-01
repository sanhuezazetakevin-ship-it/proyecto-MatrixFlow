from threading import Lock

import numpy as np
from insightface.app import FaceAnalysis

from app.core.config import settings


class EmbeddingService:
    """Carga InsightFace de forma diferida para reducir el costo de arranque en Railway.

    Se mantiene buffalo_l para no invalidar los embeddings ya registrados.
    """

    def __init__(self):
        self._model = None
        self._lock = Lock()

    @property
    def model(self) -> FaceAnalysis:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    model = FaceAnalysis(
                        name="buffalo_l",
                        providers=["CPUExecutionProvider"],
                    )
                    det_size = max(160, min(int(settings.FACE_DET_SIZE), 640))
                    model.prepare(ctx_id=-1, det_size=(det_size, det_size))
                    self._model = model
        return self._model

    def generate_embedding(self, image: np.ndarray) -> np.ndarray:
        if image is None or not isinstance(image, np.ndarray) or image.size == 0:
            raise ValueError("La imagen recibida es inválida")

        faces = self.model.get(image)
        if len(faces) == 0:
            raise ValueError("No se detectó ningún rostro")
        if len(faces) > 1:
            raise ValueError("Se detectaron varios rostros. Debe haber solamente uno.")

        embedding = faces[0].embedding
        if embedding is None:
            raise ValueError("No se pudo generar el embedding facial")

        embedding = np.asarray(embedding, dtype=np.float32).flatten()
        if embedding.shape[0] != 512:
            raise ValueError("El embedding facial generado es inválido")
        return embedding


embedding_service = EmbeddingService()
