from decimal import (
    Decimal,
    ROUND_HALF_UP,
)

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.meta_model import Meta
from app.models.sucursal_model import Sucursal
from app.models.venta_model import Venta
from app.services.audit_service import registrar_auditoria

from app.schemas.meta_schema import (
    MetaCreate,
    MetaUpdate,
)


DOS_DECIMALES = Decimal("0.01")


class MetaService:

    def _decimal(
        self,
        value,
    ) -> Decimal:
        return Decimal(str(value)).quantize(
            DOS_DECIMALES,
            rounding=ROUND_HALF_UP,
        )

    def _get_sucursal(
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
                "La sucursal indicada no existe."
            )

        if not sucursal.activo:
            raise ValueError(
                "La sucursal se encuentra inactiva."
            )

        return sucursal

    def get_by_id(
        self,
        meta_id: int,
        db: Session,
    ) -> Meta:

        meta = (
            db.query(Meta)
            .filter(Meta.id == meta_id)
            .first()
        )

        if not meta:
            raise ValueError(
                "Meta no encontrada."
            )

        return meta

    def get_all(
        self,
        db: Session,
    ) -> list[Meta]:

        return (
            db.query(Meta)
            .order_by(
                Meta.fecha_inicio.desc()
            )
            .all()
        )

    def get_by_sucursal(
        self,
        sucursal_id: int,
        db: Session,
    ) -> list[Meta]:

        self._get_sucursal(
            sucursal_id,
            db,
        )

        return (
            db.query(Meta)
            .filter(
                Meta.sucursal_id
                == sucursal_id
            )
            .order_by(
                Meta.fecha_inicio.desc()
            )
            .all()
        )

    def create(
        self,
        data: MetaCreate,
        db: Session,
        usuario_id: int | None = None,
    ) -> Meta:

        self._get_sucursal(
            data.sucursal_id,
            db,
        )

        tipo = data.tipo.strip().upper()

        if tipo != "VENTAS":
            raise ValueError(
                "Por ahora solo se admite "
                "el tipo de meta VENTAS."
            )

        existing = (
            db.query(Meta)
            .filter(
                Meta.sucursal_id
                == data.sucursal_id,
                Meta.tipo == tipo,
                Meta.fecha_inicio
                == data.fecha_inicio,
                Meta.fecha_fin
                == data.fecha_fin,
            )
            .first()
        )

        if existing:
            raise ValueError(
                "Ya existe una meta para esta "
                "sucursal, tipo y período."
            )

        meta = Meta(
            sucursal_id=data.sucursal_id,
            tipo=tipo,
            valor_objetivo=data.valor_objetivo,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
        )

        try:
            db.add(meta)

            # Necesitamos el ID antes del commit.
            db.flush()

            registrar_auditoria(
                db=db,
                usuario_id=usuario_id,
                accion="CREAR",
                entidad="meta",
                entidad_id=meta.id,
                detalle={
                    "sucursal_id": data.sucursal_id,
                    "tipo": tipo,
                    "valor_objetivo": str(
                        data.valor_objetivo
                    ),
                    "fecha_inicio": str(
                        data.fecha_inicio
                    ),
                    "fecha_fin": str(
                        data.fecha_fin
                    ),
                },
            )

            db.commit()
            db.refresh(meta)

        except Exception:
            db.rollback()
            raise

        return meta

    def update(
        self,
        meta_id: int,
        data: MetaUpdate,
        db: Session,
        usuario_id: int | None = None,
    ) -> Meta:

        meta = self.get_by_id(
            meta_id,
            db,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        fecha_inicio = values.get(
            "fecha_inicio",
            meta.fecha_inicio,
        )

        fecha_fin = values.get(
            "fecha_fin",
            meta.fecha_fin,
        )

        if fecha_fin < fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser "
                "anterior a la fecha inicial."
            )

        # Valores anteriores, para la auditoría.
        anteriores = {
            field: str(getattr(meta, field))
            for field in values
        }

        for field, value in values.items():
            setattr(
                meta,
                field,
                value,
            )

        try:
            registrar_auditoria(
                db=db,
                usuario_id=usuario_id,
                accion="ACTUALIZAR",
                entidad="meta",
                entidad_id=meta.id,
                detalle={
                    "anterior": anteriores,
                    "nuevo": {
                        field: str(value)
                        for field, value
                        in values.items()
                    },
                },
            )

            db.commit()
            db.refresh(meta)

        except Exception:
            db.rollback()
            raise

        return meta

    def cumplimiento(
        self,
        meta_id: int,
        db: Session,
    ) -> dict:

        meta = self.get_by_id(
            meta_id,
            db,
        )

        # Solo contamos ventas completadas.
        total = (
            db.query(
                func.coalesce(
                    func.sum(Venta.total),
                    0,
                )
            )
            .filter(
                Venta.sucursal_id
                == meta.sucursal_id,
                Venta.estado
                == "COMPLETADA",
                func.date(Venta.created_at)
                >= meta.fecha_inicio,
                func.date(Venta.created_at)
                <= meta.fecha_fin,
            )
            .scalar()
        )

        ventas_reales = self._decimal(
            total
        )

        objetivo = self._decimal(
            meta.valor_objetivo
        )

        diferencia = self._decimal(
            ventas_reales - objetivo
        )

        porcentaje = self._decimal(
            (
                ventas_reales
                / objetivo
            )
            * Decimal("100")
        )

        return {
            "meta_id": meta.id,
            "sucursal_id": meta.sucursal_id,
            "valor_objetivo": objetivo,
            "ventas_reales": ventas_reales,
            "diferencia": diferencia,
            "porcentaje_cumplimiento": porcentaje,
            "fecha_inicio": meta.fecha_inicio,
            "fecha_fin": meta.fecha_fin,
        }


meta_service = MetaService()