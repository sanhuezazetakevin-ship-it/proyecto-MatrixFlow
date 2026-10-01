import numpy as np


DEFAULT_FACE_THRESHOLD = 0.75
EXPECTED_EMBEDDING_SIZE = 512
_EPSILON = 1e-12


def _prepare_embedding(
    embedding: np.ndarray
) -> np.ndarray:
    """
    Valida y prepara un embedding facial para realizar
    operaciones de similitud.
    """

    if embedding is None:
        raise ValueError(
            "El embedding no puede ser None."
        )

    vector = np.asarray(
        embedding,
        dtype=np.float32
    ).reshape(-1)

    if vector.size != EXPECTED_EMBEDDING_SIZE:
        raise ValueError(
            f"El embedding debe tener "
            f"{EXPECTED_EMBEDDING_SIZE} dimensiones."
        )

    if not np.all(np.isfinite(vector)):
        raise ValueError(
            "El embedding contiene valores inválidos."
        )

    return vector


def normalize_embedding(
    embedding: np.ndarray
) -> np.ndarray:
    """
    Normaliza un embedding utilizando norma L2.
    """

    vector = _prepare_embedding(
        embedding
    )

    norm = float(
        np.linalg.norm(vector)
    )

    if norm <= _EPSILON:
        raise ValueError(
            "El embedding tiene norma cero."
        )

    return (
        vector / norm
    ).astype(
        np.float32,
        copy=False
    )


def cosine_similarity(
    embedding_a: np.ndarray,
    embedding_b: np.ndarray
) -> float:
    """
    Calcula similitud coseno entre dos embeddings.
    """

    vector_a = normalize_embedding(
        embedding_a
    )

    vector_b = normalize_embedding(
        embedding_b
    )

    similarity = float(
        np.dot(
            vector_a,
            vector_b
        )
    )

    # Protección contra pequeños errores
    # numéricos de punto flotante.
    return float(
        np.clip(
            similarity,
            -1.0,
            1.0
        )
    )


def cosine_distance(
    embedding_a: np.ndarray,
    embedding_b: np.ndarray
) -> float:
    """
    Distancia coseno = 1 - similitud coseno.
    """

    similarity = cosine_similarity(
        embedding_a,
        embedding_b
    )

    return float(
        1.0 - similarity
    )


def is_match(
    similarity: float,
    threshold: float = DEFAULT_FACE_THRESHOLD
) -> bool:
    """
    Determina si una similitud supera
    el umbral configurado.
    """

    if not np.isfinite(similarity):
        return False

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "El threshold debe estar entre 0.0 y 1.0."
        )

    return float(similarity) >= float(threshold)