import cv2
import time
import requests


API_URL = (
    "http://127.0.0.1:8000"
    "/api/auth/login-facial-liveness"
)

DNI = "70536505"

NUM_FRAMES = 5
CAPTURE_INTERVAL = 0.7


def main():

    print("=== MATRIXFLOW LOGIN FACIAL + LIVENESS ===")
    print()
    print(f"DNI: {DNI}")
    print("Mira a la cámara.")
    print("Realiza un movimiento ligero y natural.")
    print("ESC = cancelar")
    print()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "No se pudo abrir la cámara."
        )

    captured_frames = []
    last_capture = 0.0

    try:

        while len(captured_frames) < NUM_FRAMES:

            success, frame = camera.read()

            if not success:
                continue

            preview = frame.copy()

            cv2.putText(
                preview,
                (
                    f"Capturas: "
                    f"{len(captured_frames)}/{NUM_FRAMES}"
                ),
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
                "MatrixFlow - Login Facial",
                preview
            )

            current_time = time.time()

            if (
                current_time - last_capture
                >= CAPTURE_INTERVAL
            ):

                # Convertimos el frame a JPG en memoria
                success_encode, buffer = cv2.imencode(
                    ".jpg",
                    frame
                )

                if success_encode:

                    captured_frames.append(
                        buffer.tobytes()
                    )

                    print(
                        f"Frame "
                        f"{len(captured_frames)}/"
                        f"{NUM_FRAMES} capturado"
                    )

                last_capture = current_time

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                print("Login cancelado.")
                return

    finally:

        camera.release()
        cv2.destroyAllWindows()

    print()
    print("Capturas completas.")
    print("Enviando al backend...")

    # ========================================================
    # CREAR MULTIPART/FORM-DATA
    # ========================================================

    files = {}

    for index, frame_bytes in enumerate(
        captured_frames,
        start=1
    ):

        files[f"frame{index}"] = (
            f"frame{index}.jpg",
            frame_bytes,
            "image/jpeg"
        )

    data = {
        "dni": DNI
    }

    # ========================================================
    # ENVIAR AL BACKEND
    # ========================================================

    try:

        response = requests.post(
            API_URL,
            data=data,
            files=files,
            timeout=60
        )

    except requests.RequestException as error:

        print()
        print("ERROR DE CONEXIÓN:")
        print(error)
        return

    print()
    print("HTTP:", response.status_code)

    # ========================================================
    # MOSTRAR RESPUESTA
    # ========================================================

    try:

        result = response.json()

    except ValueError:

        print("Respuesta no JSON:")
        print(response.text)
        return

    if response.status_code == 200:

        print()
        print("=== LOGIN CORRECTO ===")

        print(
            "Usuario:",
            result["usuario"]["nombre"]
        )

        print(
            "Email:",
            result["usuario"]["email"]
        )

        biometria = result.get(
            "biometria",
            {}
        )

        print(
            "Similitud:",
            round(
                biometria.get(
                    "similitud",
                    0
                ),
                4
            )
        )

        print(
            "Umbral:",
            biometria.get(
                "umbral"
            )
        )

        print(
            "Cambio pose:",
            round(
                biometria.get(
                    "pose_change",
                    0
                ),
                3
            )
        )

        print(
            "Detection score:",
            round(
                biometria.get(
                    "detection_score",
                    0
                ),
                3
            )
        )

        print()
        print("JWT generado correctamente.")

        token = result.get(
            "access_token"
        )

        if token:
            print(
                "Token:",
                token[:30] + "..."
            )

    else:

        print()
        print("=== LOGIN RECHAZADO ===")

        print(
            "Detalle:",
            result.get(
                "detail",
                result
            )
        )


if __name__ == "__main__":
    main()