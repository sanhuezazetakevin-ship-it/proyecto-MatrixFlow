from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria
from app.models.empresa_model import Empresa
from app.models.producto_model import Producto

from app.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
)


class ProductoService:

    def _validar_empresa(
        self,
        empresa_id: int,
        db: Session,
    ) -> Empresa:

        empresa = (
            db.query(Empresa)
            .filter(Empresa.id == empresa_id)
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa indicada no existe."
            )

        if not empresa.activo:
            raise ValueError(
                "La empresa se encuentra inactiva."
            )

        return empresa

    def _validar_categoria(
        self,
        categoria_id: int,
        db: Session,
    ) -> Categoria:

        categoria = (
            db.query(Categoria)
            .filter(Categoria.id == categoria_id)
            .first()
        )

        if not categoria:
            raise ValueError(
                "La categoría indicada no existe."
            )

        if not categoria.activo:
            raise ValueError(
                "La categoría se encuentra inactiva."
            )

        return categoria

    def create(
        self,
        data: ProductoCreate,
        db: Session,
    ) -> Producto:

        self._validar_empresa(
            data.empresa_id,
            db,
        )

        self._validar_categoria(
            data.categoria_id,
            db,
        )

        codigo = (
            data.codigo
            .strip()
            .upper()
        )

        existing = (
            db.query(Producto)
            .filter(Producto.codigo == codigo)
            .first()
        )

        if existing:
            raise ValueError(
                "El código del producto ya está registrado."
            )

        producto = Producto(
            empresa_id=data.empresa_id,
            categoria_id=data.categoria_id,
            codigo=codigo,
            nombre=data.nombre.strip(),
            descripcion=(
                data.descripcion.strip()
                if data.descripcion
                else None
            ),
            precio=data.precio,
            costo=data.costo,
            unidad_medida=(
                data.unidad_medida
                .strip()
                .lower()
            ),
        )

        try:
            db.add(producto)
            db.commit()
            db.refresh(producto)

        except Exception:
            db.rollback()
            raise

        return producto

    def get_all(
        self,
        db: Session,
    ) -> list[Producto]:

        return (
            db.query(Producto)
            .order_by(Producto.id.asc())
            .all()
        )

    def get_by_id(
        self,
        producto_id: int,
        db: Session,
    ) -> Producto:

        producto = (
            db.query(Producto)
            .filter(Producto.id == producto_id)
            .first()
        )

        if not producto:
            raise ValueError(
                "Producto no encontrado."
            )

        return producto

    def get_by_empresa(
        self,
        empresa_id: int,
        db: Session,
    ) -> list[Producto]:

        self._validar_empresa(
            empresa_id,
            db,
        )

        return (
            db.query(Producto)
            .filter(
                Producto.empresa_id == empresa_id
            )
            .order_by(Producto.id.asc())
            .all()
        )

    def get_by_categoria(
        self,
        categoria_id: int,
        db: Session,
    ) -> list[Producto]:

        self._validar_categoria(
            categoria_id,
            db,
        )

        return (
            db.query(Producto)
            .filter(
                Producto.categoria_id == categoria_id
            )
            .order_by(Producto.id.asc())
            .all()
        )

    def update(
        self,
        producto_id: int,
        data: ProductoUpdate,
        db: Session,
    ) -> Producto:

        producto = self.get_by_id(
            producto_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        if "categoria_id" in values:
            self._validar_categoria(
                values["categoria_id"],
                db,
            )

        for field in (
            "nombre",
            "descripcion",
            "unidad_medida",
        ):
            if (
                field in values
                and values[field] is not None
            ):
                values[field] = (
                    values[field].strip()
                )

        if (
            "unidad_medida" in values
            and values["unidad_medida"]
        ):
            values["unidad_medida"] = (
                values["unidad_medida"].lower()
            )

        for field, value in values.items():
            setattr(
                producto,
                field,
                value,
            )

        try:
            db.commit()
            db.refresh(producto)

        except Exception:
            db.rollback()
            raise

        return producto


producto_service = ProductoService()