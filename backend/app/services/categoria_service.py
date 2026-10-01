from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria

from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
)


class CategoriaService:

    def create(
        self,
        data: CategoriaCreate,
        db: Session,
    ) -> Categoria:

        nombre = data.nombre.strip()

        existing = (
            db.query(Categoria)
            .filter(
                func.lower(Categoria.nombre)
                == nombre.lower()
            )
            .first()
        )

        if existing:
            raise ValueError(
                "La categoría ya está registrada."
            )

        categoria = Categoria(
            nombre=nombre,
            descripcion=(
                data.descripcion.strip()
                if data.descripcion
                else None
            ),
        )

        try:
            db.add(categoria)
            db.commit()
            db.refresh(categoria)

        except Exception:
            db.rollback()
            raise

        return categoria

    def get_all(
        self,
        db: Session,
    ) -> list[Categoria]:

        return (
            db.query(Categoria)
            .order_by(Categoria.id.asc())
            .all()
        )

    def get_by_id(
        self,
        categoria_id: int,
        db: Session,
    ) -> Categoria:

        categoria = (
            db.query(Categoria)
            .filter(
                Categoria.id == categoria_id
            )
            .first()
        )

        if not categoria:
            raise ValueError(
                "Categoría no encontrada."
            )

        return categoria

    def update(
        self,
        categoria_id: int,
        data: CategoriaUpdate,
        db: Session,
    ) -> Categoria:

        categoria = self.get_by_id(
            categoria_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        if "nombre" in values:
            nuevo_nombre = values["nombre"].strip()

            existing = (
                db.query(Categoria)
                .filter(
                    func.lower(Categoria.nombre)
                    == nuevo_nombre.lower(),
                    Categoria.id != categoria_id,
                )
                .first()
            )

            if existing:
                raise ValueError(
                    "Ya existe otra categoría con ese nombre."
                )

            values["nombre"] = nuevo_nombre

        if (
            "descripcion" in values
            and values["descripcion"] is not None
        ):
            values["descripcion"] = (
                values["descripcion"].strip()
            )

        for field, value in values.items():
            setattr(
                categoria,
                field,
                value,
            )

        try:
            db.commit()
            db.refresh(categoria)

        except Exception:
            db.rollback()
            raise

        return categoria


categoria_service = CategoriaService()