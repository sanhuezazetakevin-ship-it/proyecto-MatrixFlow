from sqlalchemy.orm import Session

from app.models.matriz_model import Matriz
from app.models.matriz_valor_model import MatrizValor

from app.schemas.matriz_schema import (
    MatrizCreate,
    MatrizUpdate,
)


class MatrizService:

    def create(
        self,
        data: MatrizCreate,
        usuario_id: int,
        db: Session,
    ) -> Matriz:

        nombre = data.nombre.strip()

        if not nombre:
            raise ValueError(
                "El nombre de la matriz es obligatorio."
            )

        filas = len(data.valores)
        columnas = len(data.valores[0])

        matriz = Matriz(
            nombre=nombre,
            descripcion=(
                data.descripcion.strip()
                if data.descripcion
                else None
            ),
            filas=filas,
            columnas=columnas,
            usuario_id=usuario_id,
        )

        try:
            db.add(matriz)

            # Obtener ID sin hacer commit.
            db.flush()

            for fila_index, fila in enumerate(
                data.valores
            ):

                for columna_index, valor in enumerate(
                    fila
                ):

                    matriz_valor = MatrizValor(
                        matriz_id=matriz.id,
                        fila=fila_index,
                        columna=columna_index,
                        valor=valor,
                    )

                    db.add(matriz_valor)

            db.commit()
            db.refresh(matriz)

        except Exception:
            db.rollback()
            raise

        return matriz

    def get_all(
        self,
        db: Session,
    ) -> list[Matriz]:

        return (
            db.query(Matriz)
            .order_by(
                Matriz.created_at.desc()
            )
            .all()
        )

    def get_by_id(
        self,
        matriz_id: int,
        db: Session,
    ) -> Matriz:

        matriz = (
            db.query(Matriz)
            .filter(
                Matriz.id == matriz_id
            )
            .first()
        )

        if not matriz:
            raise ValueError(
                "Matriz no encontrada."
            )

        return matriz

    def update(
        self,
        matriz_id: int,
        data: MatrizUpdate,
        db: Session,
    ) -> Matriz:

        matriz = self.get_by_id(
            matriz_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        if "nombre" in values:

            nombre = values["nombre"].strip()

            if not nombre:
                raise ValueError(
                    "El nombre de la matriz "
                    "no puede estar vacío."
                )

            matriz.nombre = nombre

        if "descripcion" in values:

            descripcion = values["descripcion"]

            matriz.descripcion = (
                descripcion.strip()
                if descripcion
                else None
            )

        try:
            db.commit()
            db.refresh(matriz)

        except Exception:
            db.rollback()
            raise

        return matriz

    def delete(
        self,
        matriz_id: int,
        db: Session,
    ) -> None:

        matriz = self.get_by_id(
            matriz_id,
            db,
        )

        try:
            db.delete(matriz)
            db.commit()

        except Exception:
            db.rollback()
            raise


matriz_service = MatrizService()