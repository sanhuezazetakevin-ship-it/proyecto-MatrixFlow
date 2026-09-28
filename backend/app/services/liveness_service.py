import cv2
import numpy as np

from app.services.embedding_service import embedding_service


class LivenessService:

    def __init__(self):
        self.min_detection_score = 0.65
        self.min_face_ratio = 0.10

        # Movimiento mínimo acumulado entre frames.
        self.min_pose_change = 10.0

        # Evita aceptar movimientos exagerados.
        self.max_pose_change = 45.0

        self.min_frames = 3

    # ========================================================
    # DECODIFICAR IMAGEN
    # ========================================================

    def decode_image(
        self,
        image_bytes: bytes
    ) -> np.ndarray:

        if not image_bytes:
            raise ValueError(
                "La imagen está vacía."
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

        return image

    # ========================================================
    # ANALIZAR UN FRAME
    # ========================================================

    def analyze_frame(
        self,
        image: np.ndarray
    ) -> dict:

        if image is None:
            raise ValueError(
                "Frame inválido."
            )

        faces = embedding_service.model.get(
            image
        )

        if len(faces) == 0:
            raise ValueError(
                "No se detectó ningún rostro."
            )

        if len(faces) > 1:
            raise ValueError(
                "Debe aparecer solamente una persona."
            )

        face = faces[0]

        # ----------------------------------------------------
        # Confianza de detección
        # ----------------------------------------------------

        detection_score = float(
            face.det_score
        )

        if detection_score < self.min_detection_score:
            raise ValueError(
                "La detección del rostro no tiene "
                "calidad suficiente."
            )

        # ----------------------------------------------------
        # Tamaño del rostro respecto a la imagen
        # ----------------------------------------------------

        bbox = np.asarray(
            face.bbox,
            dtype=np.float32
        )

        x1, y1, x2, y2 = bbox

        face_width = max(
            float(x2 - x1),
            0.0
        )

        face_height = max(
            float(y2 - y1),
            0.0
        )

        image_height, image_width = (
            image.shape[:2]
        )

        face_area = (
            face_width * face_height
        )

        image_area = float(
            image_width * image_height
        )

        face_ratio = (
            face_area / image_area
            if image_area > 0
            else 0.0
        )

        if face_ratio < self.min_face_ratio:
            raise ValueError(
                "Acerca un poco más el rostro "
                "a la cámara."
            )

        # ----------------------------------------------------
        # Pose facial
        # ----------------------------------------------------

        pose = np.asarray(
            face.pose,
            dtype=np.float32
        )

        # ----------------------------------------------------
        # Landmarks
        # ----------------------------------------------------

        landmarks_2d = np.asarray(
            face.landmark_2d_106,
            dtype=np.float32
        )

        landmarks_3d = np.asarray(
            face.landmark_3d_68,
            dtype=np.float32
        )

        return {
            "pose": pose,
            "det_score": detection_score,
            "face_ratio": float(face_ratio),
            "landmarks_2d": landmarks_2d,
            "landmarks_3d": landmarks_3d,
            "embedding": np.asarray(
                face.embedding,
                dtype=np.float32
            )
        }

    # ========================================================
    # COMPROBAR LIVENESS EN VARIOS FRAMES
    # ========================================================

    def verify_frames(
        self,
        images: list[np.ndarray]
    ) -> dict:

        if len(images) < self.min_frames:
            raise ValueError(
                f"Se necesitan al menos "
                f"{self.min_frames} capturas."
            )

        analyses = []

        for image in images:

            analysis = self.analyze_frame(
                image
            )

            analyses.append(
                analysis
            )

        # ----------------------------------------------------
        # Comparar cambios de pose
        # ----------------------------------------------------

        poses = [
            analysis["pose"]
            for analysis in analyses
        ]

        total_pose_change = 0.0

        for index in range(
            1,
            len(poses)
        ):

            difference = np.linalg.norm(
                poses[index] -
                poses[index - 1]
            )

            total_pose_change += float(
                difference
            )

        # ----------------------------------------------------
        # Movimiento demasiado pequeño
        # ----------------------------------------------------

        if total_pose_change < self.min_pose_change:
            return {
                "liveness": False,
                "reason": (
                    "No se detectó suficiente "
                    "variación facial entre las capturas."
                ),
                "pose_change": float(
                    total_pose_change
                )
            }

        # ----------------------------------------------------
        # Movimiento anormalmente grande
        # ----------------------------------------------------

        if total_pose_change > self.max_pose_change:
            return {
                "liveness": False,
                "reason": (
                    "Se detectó una variación "
                    "excesiva entre las capturas."
                ),
                "pose_change": float(
                    total_pose_change
                )
            }

        # ----------------------------------------------------
        # Liveness aceptado
        # ----------------------------------------------------

        best_analysis = max(
            analyses,
            key=lambda item: item["det_score"]
        )

        return {
            "liveness": True,
            "reason": "Presencia facial verificada.",
            "pose_change": float(
                total_pose_change
            ),
            "best_embedding": (
                best_analysis["embedding"]
            ),
            "detection_score": float(
                best_analysis["det_score"]
            ),
            "face_ratio": float(
                best_analysis["face_ratio"]
            )
        }


liveness_service = LivenessService()