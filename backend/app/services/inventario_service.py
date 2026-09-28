from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.inventario_model import Inventario
from app.models.movimiento_inventario_model import (
    MovimientoInventario,
)
from app.models.producto_model import Producto
from app.models.sucursal_model import Sucursal

from app.schemas.inventario_schema import (
    InventarioCreate,
    InventarioUpdate,
    MovimientoCreate,
)


TIPOS_MOVIMIENTO = {
    "ENTRADA",
    "SALIDA",
    "AJUSTE_ENTRADA",
    "AJUSTE_SALIDA",
}


class InventarioService:

    # ==================================================
    # VALIDACIONES
    # ==================================================

    def _get_sucursal(
        self,
        sucursal_id: int,
        db: Session,
    ) -> Sucursal:

        sucursal = (
            db.query(Sucursal)
            .filter(Sucursal.id == sucursal_id)
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

    def _get_producto(
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
                "El producto indicado no existe."
            )

        if not producto.activo:
            raise ValueError(
                "El producto se encuentra inactivo."
            )

        return producto

    # ==================================================
    # CREAR INVENTARIO
    # ==================================================

    def create(
        self,
        data: InventarioCreate,
        usuario_id: int,
        db: Session,
    ) -> Inventario:

        sucursal = self._get_sucursal(
            data.sucursal_id,
            db,
        )

        producto = self._get_producto(
            data.producto_id,
            db,
        )

        # El producto y la sucursal deben pertenecer
        # a la misma empresa.
        if producto.empresa_id != sucursal.empresa_id:
            raise ValueError(
                "El producto y la sucursal "
                "pertenecen a empresas diferentes."
            )

        existing = (
            db.query(Inventario)
            .filter(
                Inventario.sucursal_id
                == data.sucursal_id,
                Inventario.producto_id
                == data.producto_id,
            )
            .first()
        )

        if existing:
            raise ValueError(
                "Ya existe inventario para este "
                "producto en esta sucursal."
            )

        inventario = Inventario(
            sucursal_id=data.sucursal_id,
            producto_id=data.producto_id,
            stock_actual=data.stock_inicial,
            stock_minimo=data.stock_minimo,
        )

        try:
            db.add(inventario)

            # Necesitamos el ID antes del commit.
            db.flush()

            # Si existe stock inicial, también
            # dejamos trazabilidad.
            if data.stock_inicial > 0:

                movimiento = MovimientoInventario(
                    inventario_id=inventario.id,
                    tipo="ENTRADA",
                    cantidad=data.stock_inicial,
                    stock_anterior=Decimal("0"),
                    stock_nuevo=data.stock_inicial,
                    motivo="Stock inicial",
                    usuario_id=usuario_id,
                )

                db.add(movimiento)

            db.commit()
            db.refresh(inventario)

        except Exception:
            db.rollback()
            raise

        return inventario

    # ==================================================
    # CONSULTAS
    # ==================================================

    def get_all(
        self,
        db: Session,
    ) -> list[Inventario]:

        return (
            db.query(Inventario)
            .order_by(Inventario.id.asc())
            .all()
        )

    def get_by_id(
        self,
        inventario_id: int,
        db: Session,
    ) -> Inventario:

        inventario = (
            db.query(Inventario)
            .filter(
                Inventario.id == inventario_id
            )
            .first()
        )

        if not inventario:
            raise ValueError(
                "Inventario no encontrado."
            )

        return inventario

    def get_by_sucursal(
        self,
        sucursal_id: int,
        db: Session,
    ) -> list[Inventario]:

        self._get_sucursal(
            sucursal_id,
            db,
        )

        return (
            db.query(Inventario)
            .filter(
                Inventario.sucursal_id
                == sucursal_id
            )
            .order_by(Inventario.id.asc())
            .all()
        )

    # ==================================================
    # STOCK MÍNIMO
    # ==================================================

    def update(
        self,
        inventario_id: int,
        data: InventarioUpdate,
        db: Session,
    ) -> Inventario:

        inventario = self.get_by_id(
            inventario_id,
            db,
        )

        inventario.stock_minimo = (
            data.stock_minimo
        )

        try:
            db.commit()
            db.refresh(inventario)

        except Exception:
            db.rollback()
            raise

        return inventario

    # ==================================================
    # MOVIMIENTOS
    # ==================================================

    def registrar_movimiento(
        self,
        inventario_id: int,
        data: MovimientoCreate,
        usuario_id: int,
        db: Session,
    ) -> MovimientoInventario:

        inventario = self.get_by_id(
            inventario_id,
            db,
        )

        tipo = (
            data.tipo
            .strip()
            .upper()
        )

        if tipo not in TIPOS_MOVIMIENTO:
            raise ValueError(
                "Tipo de movimiento inválido. "
                "Use ENTRADA, SALIDA, "
                "AJUSTE_ENTRADA o AJUSTE_SALIDA."
            )

        cantidad = data.cantidad

        stock_anterior = (
            inventario.stock_actual
        )

        # ----------------------------------------------
        # CALCULAR NUEVO STOCK
        # ----------------------------------------------

        if tipo in {
            "ENTRADA",
            "AJUSTE_ENTRADA",
        }:
            stock_nuevo = (
                stock_anterior + cantidad
            )

        else:
            stock_nuevo = (
                stock_anterior - cantidad
            )

            if stock_nuevo < 0:
                raise ValueError(
                    "Stock insuficiente para "
                    "realizar la salida."
                )

        # ----------------------------------------------
        # ACTUALIZAR + REGISTRAR
        # ----------------------------------------------

        inventario.stock_actual = stock_nuevo

        movimiento = MovimientoInventario(
            inventario_id=inventario.id,
            tipo=tipo,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=(
                data.motivo.strip()
                if data.motivo
                else None
            ),
            usuario_id=usuario_id,
        )

        try:
            db.add(movimiento)

            # Un solo commit para ambas operaciones.
            db.commit()

            db.refresh(inventario)
            db.refresh(movimiento)

        except Exception:
            db.rollback()
            raise

        return movimiento

    # ==================================================
    # HISTORIAL
    # ==================================================

    def get_movimientos(
        self,
        inventario_id: int,
        db: Session,
    ) -> list[MovimientoInventario]:

        self.get_by_id(
            inventario_id,
            db,
        )

        return (
            db.query(MovimientoInventario)
            .filter(
                MovimientoInventario.inventario_id
                == inventario_id
            )
            .order_by(
                MovimientoInventario.created_at.desc()
            )
            .all()
        )


inventario_service = InventarioService()