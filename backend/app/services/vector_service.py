from sqlalchemy.orm import Session

from app.services.audit_service import registrar_auditoria

from app.models.vector_model import Vector
from app.models.vector_valor_model import VectorValor

from app.schemas.vector_schema import (
    VectorCreate,
    VectorUpdate,
)


class VectorService:

    def create(
        self,
        data: VectorCreate,
        usuario_id: int,
        db: Session,
    ) -> Vector:

        nombre = data.nombre.strip()

        if not nombre:
            raise ValueError(
                "El nombre del vector es obligatorio."
            )

        if len(data.valores) == 0:
            raise ValueError(
                "El vector debe contener al menos un valor."
            )

        vector = Vector(
            nombre=nombre,
            descripcion=(
                data.descripcion.strip()
                if data.descripcion
                else None
            ),
            dimension=len(data.valores),
            usuario_id=usuario_id,
        )

        try:
            db.add(vector)
            db.flush()

            for posicion, valor in enumerate(
                data.valores
            ):
                vector_valor = VectorValor(
                    vector_id=vector.id,
                    posicion=posicion,
                    valor=valor,
                )

                db.add(vector_valor)

            registrar_auditoria(db, usuario_id, "CREAR", "vector", vector.id, {"dimension": vector.dimension})
            db.commit()
            db.refresh(vector)

        except Exception:
            db.rollback()
            raise

        return vector

    def get_all(
        self,
        db: Session,
    ) -> list[Vector]:

        return (
            db.query(Vector)
            .order_by(
                Vector.created_at.desc()
            )
            .all()
        )

    def get_by_id(
        self,
        vector_id: int,
        db: Session,
    ) -> Vector:

        vector = (
            db.query(Vector)
            .filter(
                Vector.id == vector_id
            )
            .first()
        )

        if not vector:
            raise ValueError(
                "Vector no encontrado."
            )

        return vector

    def update(
        self,
        vector_id: int,
        data: VectorUpdate,
        db: Session,
        usuario_id: int | None = None,
    ) -> Vector:

        vector = self.get_by_id(
            vector_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        if "nombre" in values:
            nombre = values["nombre"].strip()

            if not nombre:
                raise ValueError(
                    "El nombre del vector "
                    "no puede estar vacío."
                )

            vector.nombre = nombre

        if "descripcion" in values:
            descripcion = values["descripcion"]

            vector.descripcion = (
                descripcion.strip()
                if descripcion
                else None
            )

        try:
            registrar_auditoria(db, usuario_id, "ACTUALIZAR", "vector", vector.id, {"campos": list(values.keys())})
            db.commit()
            db.refresh(vector)

        except Exception:
            db.rollback()
            raise

        return vector

    def delete(
        self,
        vector_id: int,
        db: Session,
        usuario_id: int | None = None,
    ) -> None:

        vector = self.get_by_id(
            vector_id,
            db,
        )

        try:
            registrar_auditoria(db, usuario_id, "ELIMINAR", "vector", vector.id, {"nombre": vector.nombre})
            db.delete(vector)
            db.commit()

        except Exception:
            db.rollback()
            raise


vector_service = VectorService()