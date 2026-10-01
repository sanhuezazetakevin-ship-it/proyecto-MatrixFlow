from sqlalchemy.orm import Session

from app.models.empresa_model import Empresa
from app.schemas.empresa_schema import (
    EmpresaCreate,
    EmpresaUpdate,
)


class EmpresaService:

    def create(
        self,
        data: EmpresaCreate,
        db: Session,
    ) -> Empresa:

        ruc = data.ruc.strip()

        if (
            len(ruc) != 11
            or not ruc.isdigit()
        ):
            raise ValueError(
                "El RUC debe contener exactamente 11 dígitos."
            )

        existing = (
            db.query(Empresa)
            .filter(Empresa.ruc == ruc)
            .first()
        )

        if existing:
            raise ValueError(
                "El RUC ya está registrado."
            )

        empresa = Empresa(
            ruc=ruc,
            razon_social=data.razon_social.strip(),
            nombre_comercial=(
                data.nombre_comercial.strip()
                if data.nombre_comercial
                else None
            ),
            direccion=data.direccion,
            telefono=data.telefono,
            email=(
                str(data.email).lower()
                if data.email
                else None
            ),
        )

        try:
            db.add(empresa)
            db.commit()
            db.refresh(empresa)

        except Exception:
            db.rollback()
            raise

        return empresa

    def get_all(
        self,
        db: Session,
    ) -> list[Empresa]:

        return (
            db.query(Empresa)
            .order_by(Empresa.id.asc())
            .all()
        )

    def get_by_id(
        self,
        empresa_id: int,
        db: Session,
    ) -> Empresa:

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

        return empresa

    def update(
        self,
        empresa_id: int,
        data: EmpresaUpdate,
        db: Session,
    ) -> Empresa:

        empresa = self.get_by_id(
            empresa_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        for field, value in values.items():

            if field == "email" and value:
                value = str(value).lower()

            if (
                isinstance(value, str)
                and field != "email"
            ):
                value = value.strip()

            setattr(
                empresa,
                field,
                value,
            )

        try:
            db.commit()
            db.refresh(empresa)

        except Exception:
            db.rollback()
            raise

        return empresa


empresa_service = EmpresaService()