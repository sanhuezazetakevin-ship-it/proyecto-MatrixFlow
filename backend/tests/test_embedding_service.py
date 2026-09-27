import cv2

from app.services.embedding_service import embedding_service


IMAGE_PATH = "tests/images/rostro_prueba.jpg"


def main():
    print("=== PRUEBA EMBEDDING SERVICE ===")

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print("ERROR: No se pudo cargar la imagen")
        return

    print("Imagen cargada: OK")
    print(f"Resolución: {image.shape[1]}x{image.shape[0]}")

    try:
        embedding = embedding_service.generate_embedding(image)

        print("Rostro detectado: OK")
        print("Embedding generado: OK")
        print(f"Dimensión: {embedding.shape}")
        print(f"Tipo: {embedding.dtype}")
        print("=== PRUEBA EXITOSA ===")

    except Exception as e:
        print(f"ERROR durante el procesamiento: {e}")


if __name__ == "__main__":
    main()