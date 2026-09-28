from sqlalchemy.orm import Session

from app.models.empresa_model import Empresa
from app.models.sucursal_model import Sucursal

from app.schemas.sucursal_schema import (
    SucursalCreate,
    SucursalUpdate,
)


class SucursalService:

    def create(
        self,
        data: SucursalCreate,
        db: Session,
    ) -> Sucursal:

        # ================================================
        # 1. COMPROBAR EMPRESA
        # ================================================

        empresa = (
            db.query(Empresa)
            .filter(
                Empresa.id == data.empresa_id
            )
            .first()
        )

        if not empresa:
            raise ValueError(
                "La empresa indicada no existe."
            )

        if not empresa.activo:
            raise ValueError(
                "No se pueden crear sucursales "
                "para una empresa inactiva."
            )

        # ================================================
        # 2. NORMALIZAR CÓDIGO
        # ================================================

        codigo = (
            data.codigo
            .strip()
            .upper()
        )

        # ================================================
        # 3. COMPROBAR CÓDIGO
        # ================================================

        existing = (
            db.query(Sucursal)
            .filter(
                Sucursal.codigo == codigo
            )
            .first()
        )

        if existing:
            raise ValueError(
                "El código de sucursal ya está registrado."
            )

        # ================================================
        # 4. CREAR
        # ================================================

        sucursal = Sucursal(
            empresa_id=data.empresa_id,
            nombre=data.nombre.strip(),
            codigo=codigo,
            direccion=(
                data.direccion.strip()
                if data.direccion
                else None
            ),
            ciudad=(
                data.ciudad.strip()
                if data.ciudad
                else None
            ),
            telefono=(
                data.telefono.strip()
                if data.telefono
                else None
            ),
        )

        try:
            db.add(sucursal)
            db.commit()
            db.refresh(sucursal)

        except Exception:
            db.rollback()
            raise

        return sucursal

    def get_all(
        self,
        db: Session,
    ) -> list[Sucursal]:

        return (
            db.query(Sucursal)
            .order_by(Sucursal.id.asc())
            .all()
        )

    def get_by_id(
        self,
        sucursal_id: int,
        db: Session,
    ) -> Sucursal:

        sucursal = (
            db.query(Sucursal)
            .filter(
                Sucursal.id == sucursal_id
            )
            .first()
        )

        if not sucursal:
            raise ValueError(
                "Sucursal no encontrada."
            )

        return sucursal

    def get_by_empresa(
        self,
        empresa_id: int,
        db: Session,
    ) -> list[Sucursal]:

        empresa = (
            db.query(Empresa)
            .filter(
                Empresa.id == empresa_id
            )
            .first()
        )

        if not empresa:
            raise ValueError(
                "Empresa no encontrada."
            )

        return (
            db.query(Sucursal)
            .filter(
                Sucursal.empresa_id == empresa_id
            )
            .order_by(Sucursal.id.asc())
            .all()
        )

    def update(
        self,
        sucursal_id: int,
        data: SucursalUpdate,
        db: Session,
    ) -> Sucursal:

        sucursal = self.get_by_id(
            sucursal_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        for field, value in values.items():

            if isinstance(value, str):
                value = value.strip()

            setattr(
                sucursal,
                field,
                value,
            )

        try:
            db.commit()
            db.refresh(sucursal)

        except Exception:
            db.rollback()
            raise

        return sucursal


sucursal_service = SucursalService()