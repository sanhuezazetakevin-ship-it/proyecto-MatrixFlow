import cv2

from app.services.embedding_service import embedding_service


IMAGE_PATH = "tests/images/rostro_prueba.jpg"


print("=== DATOS DEL ROSTRO ===")

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise RuntimeError(
        f"No se pudo cargar: {IMAGE_PATH}"
    )

faces = embedding_service.model.get(image)

print("Rostros detectados:", len(faces))

if len(faces) != 1:
    raise RuntimeError(
        "La prueba necesita exactamente un rostro."
    )

face = faces[0]

print("\nAtributos disponibles:")

for atributo in [
    "bbox",
    "kps",
    "landmark_2d_106",
    "landmark_3d_68",
    "pose",
    "det_score",
    "embedding"
]:
    valor = getattr(
        face,
        atributo,
        None
    )

    if valor is None:
        print(f"{atributo}: NO")
    else:
        try:
            print(
                f"{atributo}: SI - shape {valor.shape}"
            )
        except AttributeError:
            print(
                f"{atributo}: SI - {valor}"
            )

print("\n=== FIN ===")