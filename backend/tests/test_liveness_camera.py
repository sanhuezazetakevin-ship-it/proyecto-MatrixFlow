import cv2
import time
import numpy as np

from app.services.liveness_service import liveness_service


CAMERA_INDEX = 0
NUM_CAPTURES = 5
CAPTURE_INTERVAL = 0.7


def main():

    print("=== PRUEBA LIVENESS CON CÁMARA ===")
    print()
    print("Mira a la cámara y mueve ligeramente")
    print("la cabeza de forma natural.")
    print()
    print("ESC = cancelar")
    print()

    camera = cv2.VideoCapture(
        CAMERA_INDEX
    )

    if not camera.isOpened():
        raise RuntimeError(
            "No se pudo abrir la cámara."
        )

    captured_images = []
    last_capture = 0.0

    try:

        while len(captured_images) < NUM_CAPTURES:

            success, frame = camera.read()

            if not success:
                continue

            # ----------------------------------------------
            # Mostrar información
            # ----------------------------------------------

            preview = frame.copy()

            text = (
                f"Capturas: "
                f"{len(captured_images)}/"
                f"{NUM_CAPTURES}"
            )

            cv2.putText(
                preview,
                text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.putText(
                preview,
                "Mueve ligeramente la cabeza",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "MatrixFlow - Liveness",
                preview
            )

            # ----------------------------------------------
            # Captura automática
            # ----------------------------------------------

            current_time = time.time()

            if (
                current_time - last_capture
                >= CAPTURE_INTERVAL
            ):

                try:

                    analysis = (
                        liveness_service.analyze_frame(
                            frame
                        )
                    )

                    pose = analysis["pose"]

                    print(
                        f"Frame "
                        f"{len(captured_images) + 1}: "
                        f"pose={np.round(pose, 2)}, "
                        f"score="
                        f"{analysis['det_score']:.3f}, "
                        f"face_ratio="
                        f"{analysis['face_ratio']:.3f}"
                    )

                    captured_images.append(
                        frame.copy()
                    )

                    last_capture = current_time

                except ValueError as error:

                    print(
                        f"Frame descartado: {error}"
                    )

                    last_capture = current_time

            # ----------------------------------------------
            # ESC
            # ----------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                print("Prueba cancelada.")
                return

    finally:

        camera.release()
        cv2.destroyAllWindows()

    # ======================================================
    # VERIFICAR LIVENESS
    # ======================================================

    print()
    print("Analizando capturas...")

    resultado = (
        liveness_service.verify_frames(
            captured_images
        )
    )

    print()
    print("=== RESULTADO ===")
    print(
        "Liveness:",
        resultado["liveness"]
    )

    print(
        "Motivo:",
        resultado["reason"]
    )

    print(
        "Cambio de pose:",
        round(
            resultado["pose_change"],
            3
        )
    )

    if resultado["liveness"]:

        print(
            "Detection score:",
            round(
                resultado["detection_score"],
                3
            )
        )

        print(
            "Face ratio:",
            round(
                resultado["face_ratio"],
                3
            )
        )

        print(
            "Embedding:",
            resultado[
                "best_embedding"
            ].shape
        )

    print("=================")


if __name__ == "__main__":
    main()